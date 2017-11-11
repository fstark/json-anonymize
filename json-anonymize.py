import sys
import json

def num_to_string( n ):
    if n<52:
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"[n]
    return num_to_string( int(n/52) ) + num_to_string( n%52 )

class Anonymizer:
    anon_dict = { "":"" }
    counts = {}

    def next_num( self, i ):
        if not i in self.counts:
            self.counts[i] = 0
        self.counts[i] += 1
        return self.counts[i]

    def new_anon( self, o ):
        l = len(o)
        ix = self.next_num(l)
        if ix<10**l:
            s = str(ix)
        else:
            s = num_to_string(ix)
        return s.zfill(l)

    def anon_string( self, o ) :
        if not o in self.anon_dict:
            self.anon_dict[o] = self.new_anon( o )
        return self.anon_dict[o]

    def anon( self, o ):
        if o.__class__ == str:
            return self.anon_string(o)
        if o.__class__ == list:
            return [self.anon(v) for v in o]
        if o.__class__ == dict:
            r = {}
            for k, v in o.items():
                r[self.anon(k)] = self.anon(v)
            return r
        return o

i = 0
a = Anonymizer()
for arg in sys.argv[2:]:
    print( arg )
    with open(arg) as f:
        with open(str(i)+".json", "w") as file_out:
            file_out.write(json.dumps(a.anon( json.loads( f.read() ) ),separators=(',',':')))
        i += 1

