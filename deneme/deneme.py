with open("./deneme/deneme.txt") as f:
    lol=f.read()

print(lol)

lol=lol.format(fatal="cok",error="iyi",a="fdsa",b="fdas ")
print(lol)