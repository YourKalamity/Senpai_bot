
import discord
from discord.ext import commands
import sqlite3
import os
import time
from datetime import datetime
database = os.getcwd()+r"/db/database.db"
theOwner = 194852876902727680

class Database(commands.Cog):
    """Used to store data in to SQL databases using SQLLite3"""
    def __init__(self,client):
        self.client = client
        self.conn = create_connection(database)
        if self.conn is not None:
            create_table(self.conn,"""CREATE TABLE IF NOT EXISTS blacklist (
                                    user_id integer PRIMARY KEY,
                                    reason text NOT NULL,
                                    date_banned integer NOT NULL
                                );""")
            create_table(self.conn,"""CREATE TABLE IF NOT EXISTS commandlogs (
                                    id integer PRIMARY KEY,
                                    command text NOT NULL,
                                    user_id integer NOT NULL,
                                    server_id integer NOT NULL,
                                    channel_id integer NOT NULL,
                                    date_ran integer
                                );""")
            
    @commands.command()
    async def blacklist(self,ctx,member: discord.Member,*,reason=None):
        if ctx.author.id == theOwner:
            if reason==None:
                reason = "None provided"
            add_to_blacklist(self.conn,member.id,reason)
            await ctx.send(member.name+" has been blacklisted")
            channel = await member.create_dm()
            await channel.send("You have been blacklisted from this bot for :"+"\n`"+reason+"`"+"\nJoin https://discord.gg/3XBcER9 to appeal")
    
    @commands.command()
    async def unblacklist(self,ctx,member: discord.Member):
        if ctx.author.id == theOwner:
            remove_from_blacklist(self.conn,member.id)
            await ctx.send(member.name+" has been removed from the blacklist")
            channel = await member.create_dm()
            await channel.send("Your blacklist has been removed"+"\nYou may use this bot again"+"\nNext time, think twice before deciding to do something to be blacklisted.")

    @commands.command()
    async def checkblacklist(self,ctx,member: discord.Member):
        if ctx.author.id == theOwner:
            check = check_blacklist(self.conn, member.id)
            print(check)
            if check != None:
                await ctx.send(member.name + " is on the blacklist since "+datetime.utcfromtimestamp(list(check)[-1]).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                await ctx.send(member.name + " is not on the blacklist")

    @commands.command()
    async def sql(self,ctx,*,command):
        if ctx.author.id == theOwner:
            if command.startswith("```SQL"):
                command = (command[6:-3])
            rows = run_sql_query(self.conn,command)
            return_value="```\n"
            for row in rows:
                return_value = return_value + str(row) + "\n"
            return_value = return_value + "```"
            await ctx.send(return_value)
            return

            

def setup(client):
    client.add_cog(Database(client))


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def run_sql_query(conn,command):
    cur = conn.cursor()
    cur.execute(command)
    rows=cur.fetchall()
    conn.commit()
    return rows

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def add_to_blacklist(conn,user_id,reason):
    date = int(time.time())
    sql = """ INSERT INTO blacklist(user_id,reason,date_banned)
              VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql,(user_id,reason,date))
    conn.commit()
    
def remove_from_blacklist(conn,user_id):
    date = int(time.time())
    sql = """ DELETE FROM blacklist WHERE user_id = ?"""
    cur = conn.cursor()
    cur.execute(sql,(user_id,))
    conn.commit()

def check_blacklist(conn,user_id):
    
    sql = """ SELECT * FROM blacklist WHERE user_id = ? LIMIT 1;"""
    cur = conn.cursor()
    cur.execute(sql,(user_id,))
    rows = cur.fetchall()
    for row in rows:
        return row

def add_command_to_log(conn,ctx):
    sql = """ INSERT INTO commandlogs(command,user_id,server_id,channel_id,date_ran) VALUES(?,?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql,(ctx.message.content,ctx.author.id,ctx.guild.id,ctx.channel.id,ctx.message.created_at))
    conn.commit()
