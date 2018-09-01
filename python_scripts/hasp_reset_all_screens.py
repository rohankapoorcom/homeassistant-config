###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  08/31/2018
#  @name         :  hasp_reset_all_screens.py
#  @description  :  Resets to the last viewed screen
#  @params       :  All params are taken as strings from Home Assistant
#   entities: A list of input numbers that are storing the active pages
###############################################################################

def get_nodename(entity_id):
    if not entity_id.startswith('input_number.'):
        return None

    prefix = 'input_number.hasp_'
    suffix = '_activepage'
    start = entity_id.find(prefix)
    end = entity_id.find(suffix)
    if start == -1 or end == -1:
        return None
    return entity_id[(start + len(prefix)):end]

def reset_hasp_screen(hass, entity_id):
    global get_nodename
    nodename = get_nodename(entity_id)
    if not nodename:
        return

    cur_state = hass.states.get(entity_id)
    if not cur_state:
        return

    hass.services.call('mqtt', 'publish', {
        'topic': 'hasp/{}/command/page'.format(nodename),
        'payload': int(float(cur_state.state))
    })
    return

entities = data.get('entities')

if isinstance(entities, str):
    entities = [e.strip() for e in entities.split(',')]
    for entity_id in entities:
        reset_hasp_screen(hass, entity_id)
