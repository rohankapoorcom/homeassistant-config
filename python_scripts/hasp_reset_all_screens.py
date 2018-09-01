###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  08/31/2018
#  @name         :  hasp_reset_all_screens.py
#  @description  :  Handles publishing new text with the correct font size
#                   adjustments for a HASP device
#  @params       :  All params are taken as strings from Home Assistant
#   entity_ids: A list of input numbers that are storing the active pages
###############################################################################

def get_nodename(entity_id):
    if not entity_id.startswith('input_number.'):
        return None

    start = entity_id.find('input_number.') + 13
    end = entity_id.find('_activepage')
    if start == -1 or end == -1:
        return None
    return entity_id[start:end]

def reset_hasp_screen(entity_id):
    nodename = get_nodename(entity_id)
    if not nodename:
        return

    cur_state = hass.state.get(entity_id)
    if not cur_state:
        return

    hass.services.call('mqtt', 'publish', {
        'topic': 'hasp/{}/command/page'.format(nodename),
        'payload': cur_state.state
    })

entities = data.get('entities')

if isinstance(entity_id, str):
    entities = [e.strip() for e in entity_id.split(',')]
    for entity_id in entities:
        reset_hasp_screen(entity_id)
