###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  09/07/2018
#  @name         :  media_music_turn_off_speakers
#  @description  :  Turns off speakers specified
#  @params       :  All params are taken as strings from Home Assistant
#   entities: A list of remote entities that should be turned off
###############################################################################


def decrement_speakers_playing(hass):
    entity_id = 'input_number.speakers_playing'
    speakers_playing = hass.states.get(entity_id)
    if not (
        speakers_playing
        and speakers_playing.attributes
        and speakers_playing.attributes.get('min') is not None
    ):
        return
    count = int(float(speakers_playing.state))
    if count > int(float(speakers_playing.attributes.get('min'))):
        count = count - 1
    hass.services.call('input_number', 'set_value', {
                           'value': count,
                           'entity_id': entity_id
                           }
                       )


def turn_off_speaker(hass, entity_id):
    cur_state = hass.states.get(entity_id)
    if not (cur_state
            and cur_state.attributes
            and cur_state.attributes.get('current_activity') is not None
            and cur_state.attributes.get('music_activity_name') is not None
            and cur_state.attributes.get('music_activity_name') == cur_state.attributes.get('current_activity')
    ):
        return False

    hass.services.call('remote', 'turn_off', {'entity_id': entity_id})
    return True


entities = data.get('entities')

if isinstance(entities, str):
    entities = [e.strip() for e in entities.split(',')]
    for entity in entities:
        if turn_off_speaker(hass, entity):
            decrement_speakers_playing(hass)
