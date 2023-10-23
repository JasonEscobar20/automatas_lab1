from django.shortcuts import render


# Create your views here.
def index_view(request):

    return render(request, 'core/index.html')

def get_content(line):
    content = line

    if '{' in line:
        first_square_bracket_index = line.index('{') + 1
        content = line[first_square_bracket_index: -1]
        content = content.replace('}', '')

        content = content.split(',') if 'W=' not in line else content
    else:
        equals_index = line.index('=') + 1
        content = line[equals_index:]

    return content

def get_transition_list(transition, quintupla, alphabet):
    transition_list = []
    split_transition = transition.split('),')
    result = []
    
    for item in split_transition:
        remove_parenthesis = item.replace('(', '').replace(')', '')
        transition_list.append(remove_parenthesis.split(','))

    for index, value in enumerate(quintupla):
        state = value
        result.append([state])
        states_by_letter = {}
        
        for x in alphabet:
            verify = states_by_letter.get(x, 0)
            if verify == 0:
                states_by_letter[x] = []

        for item in transition_list:
            state_to_evaluate = item[0]
            letter = item [1]
            result_state = item[2]
            
            verify = states_by_letter.get(letter, 0)
            if verify == 0:
                states_by_letter[letter] = []
        
            if state == state_to_evaluate:
                states_by_letter[letter].append(result_state)
        
        result[index].append(states_by_letter.values())
    
    return result

def split_transition_func(data):
    split_transition = data.split('),')
    transition_list = []
    
    for item in split_transition:
        remove_parenthesis = item.replace('(', '').replace(')', '')
        transition_list.append(remove_parenthesis.split(','))

    return transition_list

def get_epsilon_states(transition):
    # split_transition = transition.split('),')
    transition_list = split_transition_func(transition)
    epsilon_states = []
    
    for item in transition_list:
        state_to_evaluate = item[0]
        letter = item [1]
        result_state = item[2]
        
        if letter == 'e':
            epsilon_states.append(result_state)
    
    return epsilon_states

def move_function(item, states_no_checked, finally_states, compositions, data):
    alphabet = data['alphabet']
    
    if 'e' in data['alphabet']:
        alphabet.remove('e')
    
    state = item['state']
    new_state = item.copy()
    composition = item['composition']

    state_letter = ord(state[0])
    transition_table = data['transition_line']

    transition_table = split_transition_func(transition_table)
    get_result_states = []
    
    for character in alphabet:
        new_composition = []
        
        for item_1 in transition_table:
            first_state = item_1[0]
            letter = item_1[1]
            result_state = item_1[2]
            
            for item_2 in composition:
                if item_2 == first_state and letter == character:
                    if result_state not in new_composition:
                        new_composition.append(result_state)
                         
            
     
        for item_3 in transition_table:
            first_state = item_3[0]
            letter = item_3[1]
            result_state = item_3[2]
            
            for item_4 in new_composition:
                if item_4 == first_state and letter == 'e':
                    if result_state not in new_composition:
                        new_composition.append(result_state)
            
        new_composition.sort()
        
        if new_composition not in compositions:
            state_letter += 1
            for verify_state in states_no_checked:
                
                if verify_state['state'] == chr(state_letter):
                    state_letter += 1
                    
            next_letter = chr(state_letter)
            get_result_states.append([character, next_letter.upper()])
            
            states_no_checked.append({
                'state': next_letter,
                'composition': new_composition,
            })
            compositions.append(new_composition)
        else:
            get_state_letter = chr(state_letter).upper()
            for verify_item_exist in finally_states:
                if verify_item_exist['composition'] == new_composition:
                    get_state_letter = verify_item_exist['state'].upper()
                    
            get_result_states.append([character, get_state_letter])
    
    new_state['letters'] = get_result_states
    finally_states.append(new_state)

    for index in range(len(states_no_checked)):
        if states_no_checked[index]['state'] == state:
            del states_no_checked[index]
            break
        

def transform_afn_to_afd(data):
    transition_list = data['transition_line']
    initial_state = data['initial_state']
    epsilon_states = get_epsilon_states(transition_list)
    first_state = 'a'
    first_composition = [initial_state, *epsilon_states]
    compositions = [first_composition]
    states_no_checked = []
    finally_states = []
    
    first_item = {
        'state': first_state,
        'composition': first_composition,
    }
    
    states_no_checked.append(first_item)
    
    while len(states_no_checked) != 0:
        for item in states_no_checked:
            move_function(item, states_no_checked, finally_states, compositions, data)
            break

    afd_quintupla = [item['state'] for item in finally_states]
    afd_alphabet = data['alphabet']
    afd_initial_state = finally_states[0]['state']
    afd_success_states = []
    
    for success_state in data['success_state']:
        for item in finally_states:
            if success_state in item['composition']:
                afd_success_states.append(item['state'])
                          

    return finally_states

def result_view(request):
    get_file = request.FILES['filename']
    get_data = read_txt(get_file)
    
    get_afd = transform_afn_to_afd(get_data)
    
    
    return render(request, 'core/index.html', {
        'txt_lines': get_data['txt_lines'],
        'data': get_data,
        'afd_data': get_afd,
        'transition_array': get_data['transition_array']
    })
 

def read_txt(file):    
    test = [line.rstrip() for line in file]
    data = {}
    txt_lines = []
    quintupla = []

    for line in test:
        decode_line = line.decode()
        txt_lines.append(decode_line)

        if 'Q=' in decode_line:
            quintupla = get_content(decode_line)
            quintupla = quintupla
            data['quintupla'] = quintupla
            continue
        if 'F=' in decode_line:
            alphabet = get_content(decode_line)
            data['alphabet'] = alphabet
            continue
        if 'i=' in decode_line:
            initial_state = get_content(decode_line)
            data['initial_state'] = initial_state
            continue
        if 'A=' in decode_line:
            success_state = get_content(decode_line)
            data['success_state'] = success_state
            continue
        if 'W=' in decode_line:
            transition = get_content(decode_line)
            data['transition_line'] = transition
            transition_array = get_transition_list(transition, quintupla, alphabet)
            data['transition_array'] = transition_array
            # print(transition_array)
            continue
    
    data['txt_lines'] = txt_lines

    return data
    
    
    
