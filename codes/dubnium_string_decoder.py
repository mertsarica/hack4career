# Dubnium String Decoder v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import time
func_addr = "sub_1144CC9" # Code reuse function
xref_addr = 0x1147036 # Decode function
mod_addr = 0x00000000 # Modification address 
jmp_addr = 0x00000000 # Jump after decode function
jmp_endaddr = 0x00000000 # Jump to the reuse function
enc_arr = [] # Encoded strings
enc_addr = [] # Encoded string addresses
debug = 0 # Print useless stuff
encstr = "" # Encoded string

def set_breakpoint(addr):
  if debug:
    print "set_breakpoint(addr)"
    print "Setting breakpoint:", hex(addr)
  idc.AddBpt(addr)

# Find the beginning of code reuse function
def find_boundary():
  global jmp_endaddr
  if debug:
    print "find_boundary()"

  funcea = LocByName(func_addr)
  f = idaapi.get_func(funcea)
  set_breakpoint(f.startEA)
  jmp_endaddr = f.startEA

# Replacing encoded string with the next encoded string
def patch(addr):
  if debug:
    print "patch(addr)"

  global mod_addr
  i = 0
  if debug:
    print "Before patched:", mod_addr+i, hex(Byte(mod_addr+i)), hex(Dword(mod_addr)), GetDisasm(mod_addr)
  while i < 4:
        # Patch only the debugged process memory
	PatchDbgByte(mod_addr+i, int(hex(Byte(addr+i)), 16));
        i = i + 1
  if debug:
    print "After patched:", GetDisasm(mod_addr), hex(Dword(mod_addr))

# Find code reuse block
def find_function():
  if debug:
    print "find_function()"

  global mod_addr
  global jmp_addr
  # global jmp_endaddr
  for x in XrefsTo(xref_addr, flags=0):
    addr = idc.PrevHead(x.frm)
    if GetMnem(addr) == "push" and "105" in GetOpnd(addr, 0):
      jmp_addr = idc.NextHead(x.frm)
      jmp_addr = idc.NextHead(x.frm)
      print "Jump End Address:", hex(jmp_addr)
      set_breakpoint(jmp_addr)
      addr = idc.PrevHead(addr)
      addr = idc.PrevHead(addr)
      print "Modification Address:", hex(addr)
      mod_addr = addr

# Find encrypted strings and addresses
def find_encstr():
  if debug:
    print "find_encstr()"

  global enc_arr
  global encstr
  for x in XrefsTo(xref_addr, flags=0):
    i = 0
    patched = 0
    while i < 5:
      addr = idc.PrevHead(x.frm)
      if GetMnem(addr) == "mov" and "ecx" in GetOpnd(addr, 0):
        addr = idc.PrevHead(x.frm)
        encstr = GetOperandValue(addr, 1)
        if debug:
          print "Address: %s Encoded String: %s" % (hex(addr), get_string(encstr))
        # patch(addr)
        enc_arr.append(addr)
        enc_addr.append(GetOperandValue(addr, 1))
        break
      i = i + 1

# Let's decode the first encoded string
def start():
  if debug:
    print "start()"
  event = GetDebuggerEvent(WFNE_ANY|WFNE_CONT, -1)
  event = GetDebuggerEvent(WFNE_ANY|WFNE_CONT, -1)
  event = GetDebuggerEvent(WFNE_ANY|WFNE_CONT, -1)
  # SetRegValue(jmp_endaddr, 'EIP')
  decstr = get_string(GetRegValue('edi'))
  encstr = GetOperandValue(mod_addr, 1)
  print "Encoded String: %s Decoded String: %s" % (get_string(encstr), decstr)
  SetRegValue(jmp_endaddr, 'EIP')

# Time to decode encoded strings
def find_decstr(index):
  global jmp_endaddr
  global enc_addr
  if debug:
    print "find_decstr()"

  event = GetDebuggerEvent(WFNE_ANY|WFNE_CONT, -1)
  event = GetDebuggerEvent(WFNE_ANY|WFNE_CONT, -1)
  decstr = get_string(GetRegValue('edi'))
  encstr = GetOperandValue(mod_addr, 1)
  print "Address: %s | Encoded String: %s | Decoded String: %s" % (hex(enc_addr[index]), get_string(encstr), decstr)
  SetRegValue(jmp_endaddr, 'EIP')

# Show me the human readable string
def get_string(addr):
  if debug:
    print "get_string(addr)"

  out = ""
  while True:
    if Byte(addr) != 0:
      out += chr(Byte(addr))
    else:
      break
    addr += 1
  return out

# Main functions
find_function()
find_encstr()
find_boundary()
start()

# Patch encoded string with the next encoded one, decode it and then show it to me ;)
m = 0
for i in enc_arr:
  patch(i)
  find_decstr(m)
  m = m + 1
#  time.sleep(1)

print "Decoded %s strings" % (m)
