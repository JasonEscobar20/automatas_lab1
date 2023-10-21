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
    transition_list = []
    
    for item in data:
        remove_parenthesis = item.replace('(', '').replace(')', '')
        transition_list.append(remove_parenthesis.split(','))

    return transition_list

def get_epsilon_states(transition):
    split_transition = transition.split('),')
    transition_list = split_transition_func(split_transition)
    epsilon_states = []
    
    for item in transition_list:
        state_to_evaluate = item[0]
        letter = item [1]
        result_state = item[2]
        
        if letter == 'e':
            epsilon_states.append(result_state)
    
    return epsilon_states

def move_function(item, states_no_checked, compositions, data):
    alphabet = data['alphabet']
    alphabet.remove('e')
    
    state = item['state']
    composition = item['composition']
    print(composition)
    
    transition_table = data['transition_line']
    epsilon_states = get_epsilon_states(transition_table)
    split_transition = transition_table.split('),')
    transition_table = split_transition_func(split_transition)
    
    pruebitas = []
    
    for character in alphabet:
        for x in composition:
            for y in transition_table:
                first_state = y[0]
                letter = y [1]
                result_state = y[2]
                
                if x == first_state and letter == character:
                    pruebitas.append(result_state)
                # print(first_state, letter, result_state)
            
            
            
            # if state == first_state and letter == character:
            #     print(result_state)
    
    for x in epsilon_states:
        if x not in pruebitas:
            pruebitas.append(x)
            
    pruebitas.sort()
    
    if pruebitas not in compositions:
        i = ord(state[0])
        i+=1
        print(chr(i), 'letra siguiente')
        
    states_no_checked.remove(item)
        

def transform_afn_to_afd(data):
    transition_list = data['transition_line']
    initial_state = data['initial_state']
    epsilon_states = get_epsilon_states(transition_list)
    first_state = 'a'
    first_composition = [initial_state, *epsilon_states]
    compositions = [first_composition]
    states_no_checked = []
    
    first_item = {
        'state': first_state,
        'composition': first_composition
    }
    
    states_no_checked.append(first_item)
    
    while len(states_no_checked) != 0:
        for x in states_no_checked:
            state = x['state']
            move_function(x, states_no_checked, compositions, data)
            
        # states_no_checked.pop()
        
    
    nuevos_estados = []
    
    print(epsilon_states)

def result_view(request):
    get_file = request.FILES['filename']
    get_data = read_txt(get_file)
    
    transform_afn_to_afd(get_data)
    
    return render(request, 'core/index.html', {
        'txt_lines': get_data['txt_lines'],
        'data': get_data,
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
    
    
    
