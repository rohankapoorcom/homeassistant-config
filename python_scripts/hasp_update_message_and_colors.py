###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  05/05/2019
#  @name         :  hasp_update_message.py
#  @description  :  A wrapper to publish new text and color changes for a HASP
#                   device.
#  @params       :  All params are taken as strings from Home Assistant
#   nodename: the name of the hasp device, eg: plat01
#   object_id: the id of the object on the HASP you want to update, eg: p[2].b[5]
#   text: the text that should be sent to the HASP device
#   update_font: Update the font when updating the text (defaults to true)
#   background: the color to display on the background on the HASP device
#   foreground: the color to display on the foreground on the HASP device
###############################################################################


nodename = data.get('nodename')
object_id = data.get('object_id')
text = data.get('text')
update_font = data.get('update_font')
background = data.get('background')
foreground = data.get('foreground')

base_payload = {
    'nodename': nodename,
    'object_id': object_id,
}

if 'text' in data:
    payload = base_payload.copy()
    payload.update({
        'text': text,
        'update_font': update_font
    })
    hass.services.call('python_script', 'hasp_update_message', payload)

if background or foreground:
    payload = base_payload.copy()
    payload.update({
        'background': background,
        'foreground': foreground
    })
    hass.services.call('python_script', 'hasp_update_colors', payload)
