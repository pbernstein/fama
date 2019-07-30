import sys

def underscore_to_camelcase(value):
    def camelcase(): 
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

f = open("advfn_attributes.dat")
o = open("advfn_attributes.dat.out","w")

for line in f:
    at = line.split("|")[0].replace(" ","_").replace(",","").replace(";","").replace("  ","_")
    cc = underscore_to_camelcase(at)
    o.write(line.replace("\n","")+"|"+cc+"\n")

f.close()
o.close()

	
