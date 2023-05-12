import re

jokes = []

for n in range(1, 101):
    with open(f"jokes/init{n}.html", 'r') as jokef:
        html = jokef.read()
    pattern = re.compile("<!--begin of joke -->(.*)<!--end of joke -->",
                         flags=re.DOTALL)
    jokes.append(re.search(pattern, html).group(1)
                 .replace("\n", "")
                 .replace("<p>", "\n")
                 .replace("<P>", "\n")
                 .replace("</p>", "")
                 .replace("</P>", "")
                 )

if __name__ == "__main__":
    print("First joke:")
    print(jokes[0])
