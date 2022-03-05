import httpx, json, itertools
from colorama import init, Fore

init()

__CONFIG__ = json.load(open("config.json"))
__PROXIES__ = itertools.cycle(open(__CONFIG__["path_proxies"]).read().splitlines())


def checkServer(server):
    error = False
    if 'discord.com/invite' in server:
        code = server.split('invite/')[-1]
    elif 'discord.gg' in server:
        code = server.split("discord.gg/")[-1]
    else: 
        print(Fore.LIGHTRED_EX + "Invalid Invite: " + server + Fore.RESET)

    if __CONFIG__["use_proxies"] == "true":
        with httpx.Client(proxies="http://" + next(__PROXIES__)) as client:
            response = client.get(
                "https://discord.com/api/v9/invites/"
                + code
                + "?with_counts=true"
            )

            if 'Unknown Invite' in str(response.json()) or 'Not Found' in str(response.json()) or 'You are being rate limited' in str(response.content):
                error = True

            else:
                name = response.json()["guild"]["name"]
                members = response.json()["approximate_member_count"]

    else:
        response = httpx.get(
            "https://discord.com/api/v9/invites/"
            + code
            + "?with_counts=true"
        )

        if "Unknown Invite" in str(response.json()) or 'Not Found' in str(response.json()) or 'You are being rate limited' in str(response.content):
            error = True
        
        else:
            name = response.json()["guild"]["name"]
            members = response.json()["approximate_member_count"]
            

    if error == False and members >= __CONFIG__["max_members"]:
        print(
            Fore.LIGHTRED_EX
            + "Too many members: "
            + Fore.RESET
            + server
            + ' - '
            + name
            + " - "
            + str(members)
            + " members "
        )

        if __CONFIG__['save_too_many_members'] == "true":
            with open(__CONFIG__["path_too_many_members"], "a") as f:
                f.write(server + "\n")

    elif error == False and members <= __CONFIG__["min_members"]:
        print(
            Fore.LIGHTRED_EX
            + "Too few members: "
            + Fore.RESET
            + server
            + ' - '
            + name
            + " - "
            + str(members)
            + " members "
        )

        if __CONFIG__['save_too_few_members'] == "true":
            with open(__CONFIG__["path_too_few_members"], "a") as f:
                f.write(server + "\n")
    
    elif error:
        print(Fore.LIGHTRED_EX + "Error: " + Fore.RESET + str(response.json()))
        if __CONFIG__['save_invalid'] == "true":
            with open(__CONFIG__["path_invalid"], "a") as f:
                f.write(server + "\n")
    
    else:
        print(Fore.LIGHTGREEN_EX + "New server: " + Fore.RESET + server + ' - ' + name + ' - ' + str(members))
        if __CONFIG__['save_valid'] == "true":
            with open(__CONFIG__["path_valid"], "a") as f:
                f.write(server + "\n")

def main():
    print(
        Fore.LIGHTRED_EX
        + """
░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗██╗░░░██╗ by https://github.com/Mewzax
██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝╚██╗░██╔╝
██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░░╚████╔╝░
██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░░░╚██╔╝░░
╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗░░░██║░░░
░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░
                        Discord Invite Checker
"""     
        + Fore.RESET
    )
    servers = open(__CONFIG__["path_servers"]).read().splitlines()
    for server in servers:
        checkServer(server)

if __name__ == "__main__":
    main()