import logging
import time
import argparse
import os

__version__ = '0.1-dev'

#Usage: python Main.py --rom lttpromtobepatched.sfc #generates lttpromtobepatched_edit_[time].sfc
#General rom patching logic copied from https://github.com/LLCoolDave/ALttPEntranceRandomizer
#		Memory Address	Value
# ICONS		
# Full Heart:	0x06FA27	A0
# Half Heart:   0x06FA25	A1
# Empty Heart:	0x06FA21	A2
# New Heart:	0x06FA29	A3
# Zero:				90
# One:				91
# Two:				92
# Four:				94
# Eight:			98

# COLORS
# Black:	22
# Green:	3C
# Red:		24
# Yellow:	28

# TOGGLES
# Heart Beep:	0x180033	0x20
#  Off:		0x00
#  Normal:	0x20
#  Half:	0x40
#  Quarter:	0x80
# SRAM Trace:	0x180030	0x00
#  Off:		0x00
#  On:		0x01

def write_byte(rom, address, value):
    rom[address] = value

def calc_sprite(sprite):
  logger.debug(' ' + sprite.capitalize())
  value = 0xA0
  if sprite == "full":
    value = 0xA0
  elif sprite == "half":
    value = 0xA1
  elif sprite == "empty":
    value = 0xA2
  elif sprite == "new":
    value = 0xA3
  elif sprite == "zero":
    value = 0x90
  elif sprite == "one":
    value = 0x91
  elif sprite == "two":
    value = 0x92
  elif sprite == "four":
    value = 0x94
  elif sprite == "eight":
    value = 0x98
  else:
    value = 0xA0
  
  return value

def calc_color(color,sprite):
  value = 0x24
  if color == "black":
    value = 0x20
  elif color == "green":
    value = 0x3C
  elif color == "red":
    value = 0x24
  elif color == "yellow":
    value = 0x28
  else:
    value = 0x24
    
  if sprite == "empty":
    value = 0x24
    color = "Black"
    
  if sprite == "eight" or sprite == "four" or sprite == "two" or sprite == "one" or sprite == "zero":
    value = 0x24
    color = "White"

  logger.debug(' ' + color.capitalize())

  return value

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--loglevel',		default='info',		const='info',	nargs='?',	choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--rom', help='Path to a lttp rom to be patched.')
    parser.add_argument('--heartbeep',		default='normal',	const='info',	nargs='?',	choices=['normal','off','half','quarter','double'],			help='Heart Beep Speed')
    parser.add_argument('--fullSprite',		default='full',		const='info',	nargs='?',	choices=['full','half','empty','new','zero','one','two','four','eight'],help='Full Heart Sprite')
    parser.add_argument('--halfSprite',		default='half',		const='info',	nargs='?',	choices=['full','half','empty','new','zero','one','two','four','eight'],help='Half Heart Sprite')
    parser.add_argument('--emptySprite',	default='empty',	const='info',	nargs='?',	choices=['full','half','empty','new','zero','one','two','four','eight'],help='Empty Heart Sprite')
    parser.add_argument('--newSprite',		default='new',		const='info',	nargs='?',	choices=['full','half','empty','new','zero','one','two','four','eight'],help='New Heart Sprite')
    parser.add_argument('--fullColor',		default='red',		const='info',	nargs='?',	choices=['black','green','red','yellow'],				help='Full Heart Color')
    parser.add_argument('--halfColor',		default='red',		const='info',	nargs='?',	choices=['black','green','red','yellow'],				help='Half Heart Color')
    parser.add_argument('--emptyColor',		default='black',	const='info',	nargs='?',	choices=['black','green','red','yellow'],				help='Empty Heart Color')
    parser.add_argument('--newColor',		default='red',		const='info',	nargs='?',	choices=['black','green','red','yellow'],				help='New Heart Color')
    parser.add_argument('--sramTrace',		default='off',		const='info',	nargs='?',	choices=['off','on'],							help='SRAM Trace')
    parser.add_argument('--frameAdvance',	default='off',		const='info',	nargs='?',	choices=['off','on'],							help='Frame Advance')
    args = parser.parse_args()

    if args.rom is None:
        input('No rom specified. Please run with -h to see help for further information. \nPress Enter to exit.')
        exit(1)
    if not os.path.isfile(args.rom):
        input('Could not find valid rom for patching at path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    logger = logging.getLogger('')

    logger.info('Patching ROM.')

    rom = bytearray(open(args.rom, 'rb').read())

    # HEART BEEP
    byte	= 0x180033
    value	= 0x20
    logger.debug('')
    logger.debug("Heart Beep:")
    logger.debug(' ' + args.heartbeep.capitalize())
    if args.heartbeep	== "off":
      value = 0x00
    elif args.heartbeep	== "half":
      value = 0x40
    elif args.heartbeep	== "quarter":
      value = 0x80
    elif args.heartbeep	== "double":
      value = 0x10
    else:
      value = 0x20
    write_byte(rom,byte,value)
    
    logger.debug('')

    # SRAM TRACE
    byte 	= 0x180030
    value	= 0x01 if args.sramTrace == 'on' else 0x00
    write_byte(rom,byte,value)
    logger.debug("SRAM Trace:")
    logger.debug(' ' + str("On" if args.sramTrace == "on" else "Off"))

    logger.debug('')

    # FRAME ADVANCE
    byte 	= 0x39
    value	= 0xEA if args.frameAdvance == 'on' else 0x80
    write_byte(rom,byte,value)
    byte 	= 0x3A
    value	= 0xEA if args.frameAdvance == 'on' else 0x16
    write_byte(rom,byte,value)
    logger.debug("Frame Advance:")
    logger.debug(' ' + str("On" if args.frameAdvance == "on" else "Off"))

    logger.debug('')

    # HEART SPRITES & COLORS
    # Full Heart Sprite
    logger.debug("Full Heart: ")
    byte	= 0x06FA27
    value	= calc_sprite(args.fullSprite)
    write_byte(rom,byte,value)
    # Full Heart Color
    value	= calc_color(args.fullColor,args.fullSprite)
    write_byte(rom,byte+1,value)

    logger.debug('')

    # Half Heart Sprite
    logger.debug("Half Heart: ")
    byte	= 0x06FA25
    value	= calc_sprite(args.halfSprite)
    write_byte(rom,byte,value)
    # Half Heart Color
    value	= calc_color(args.halfColor,args.halfSprite)
    write_byte(rom,byte+1,value)

    logger.debug('')

    # Empty Heart Sprite
    logger.debug("Empty Heart: ")
    byte	= 0x06FA21
    value	= calc_sprite(args.emptySprite)
    write_byte(rom,byte,value)
    # Empty Heart Color
    value	= calc_color(args.emptyColor,args.emptySprite)
    write_byte(rom,byte+1,value)

    logger.debug('')

    # New Heart Sprite
    logger.debug("New Heart: ")
    byte	= 0x06FA29
    value	= calc_sprite(args.newSprite)
    write_byte(rom,byte,value)
    # New Heart Color
    value	= calc_color(args.newColor,args.newSprite)
    write_byte(rom,byte+1,value)

    outfilename = '%s' % (os.path.basename(args.rom).replace(".sfc","") + "_edit_" + str(int(time.time())) + ".sfc")
    logger.info("Output to: " + outfilename)

    with open('%s' % outfilename, 'wb') as outfile:
        outfile.write(rom)

    logger.info('Done.')
