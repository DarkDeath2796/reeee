try:
    import discord
    from discord.ext import commands
    import sys
    import os
    import re
    import random

    sys.set_int_max_str_digits(218798789)

    bot = commands.Bot(command_prefix='y ', intents=discord.Intents.all())

    token = ''

    async def create_and_attach(ctx, content = "0", fname = "file"):
        """
        Creates a text file, attaches it to the Discord message, and then deletes the file.
        The content is taken from command arguments.
        """
        try:
            file_path = "temp_file.txt"  # Temporary file name
            with open(file_path, 'w') as f:
                f.write(content)
                f.close()
            
            with open(file_path, 'r') as f:
                file = discord.File(f, filename=f"{fname}.txt")
                f.close()

            await ctx.send(file=file)

        except Exception as e:
            print(e)
        finally:
            try:
                os.remove(file_path)  # Remove the file
                print(f"Deleted temporary file: {file_path}") #DEBUG
            except FileNotFoundError:
                print(f"File not found for removal: {file_path}") #DEBUG
            except Exception as e:
                print(f"Error during file removal: {e}") #DEBUG

    @bot.command(name="ping")
    async def ping(ctx):
        await ctx.send("pong")
        
    @bot.command(name="express")
    async def express(ctx, *exp):
        """
        Processes multiple expressions using eval after filtering out blocked characters with regex
        Improved troll protection.
        """
        # More robust regex for blocking common dangerous patterns
        blocked_chars = r"[;`]|print|import|os|subprocess|system|exec|eval|open|read|write|\b(exec|eval|open|system)\b"

        try:
            for expression in exp:
                # Case-insensitive check and trim whitespace
                expression = expression.strip().lower()

                if re.search(blocked_chars, expression):
                    await ctx.send(f"nu uh")
                    print(f"Blocked character or keyword detected in expression '{expression}'.")
                    continue

                try:
                    res = eval(expression)
                    if not len(str(res)) > 2000:
                        await ctx.send(f"```{expression}: {res}```")
                    else:
                        await create_and_attach(ctx, content=f"{expression}: {res}", fname="result")
                except (SyntaxError, NameError, TypeError) as e:
                    await ctx.send(f"error evaluating '{expression}': {type(e).__name__}")
        except Exception as e:
            await ctx.send(f"an unexpected error occurred: {type(e).__name__}")
            print(f"Unexpected error: {e}")
            
    @bot.command(name="factorial")
    async def factorial(ctx, n):
        try:
            res = 1
            for i in range(int(n)):
                res *= i+1
            if not len(str(res)) > 2000:
                await ctx.send(res)
            else:
                await create_and_attach(ctx, content=str(res), fname="factorial") 
        except Exception as e:
            await ctx.send(f"uh oh something went wrong")
            print(e)
            
    @bot.command(name="hm")
    async def hm(ctx):
        await ctx.send("hmmmmmm")
        
    @bot.command(name="randomnum")
    async def randomnum(ctx, start, end):
        await ctx.send(str(random.randint(int(start), int(end))))

    bot.run(token)
except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.close()
            
