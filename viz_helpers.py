import numpy as np


def normalize(rgb):
    return tuple(np.array(rgb) / 255) + (1.0, )

COLOR_RED = normalize([178, 34, 34])
COLOR_BLUE = normalize([31, 120, 180])
COLOR_GREY = normalize([220, 220, 220])
COLOR_BLACK = normalize([37, 37, 37])
COLOR_YELLOW = normalize([255, 217, 47])
COLOR_WHITE = normalize([255, 255, 255])
COLOR_ORANGE = normalize([252, 120, 88])
COLOR_PINK = normalize([255, 20, 147])
COLOR_GREEN = normalize([50, 205, 50])


def default_setting(g):
    vertex_text = g.new_vertex_property('string')
    for i in range(g.num_vertices()):
        vertex_text[i] = str(i)

    vertex_fill_color = g.new_vertex_property('vector<float>')
    vertex_fill_color.set_value(COLOR_RED)

    edge_color = g.new_edge_property('vector<float>')
    edge_color.set_value(COLOR_GREY)

    edge_text = g.new_edge_property('string')
    edge_text.set_value('')

    eorder = g.new_edge_property('int')
    eorder.set_value(0)
    
    return {'vertex_text': vertex_text,
            'vertex_fill_color': vertex_fill_color,
            'vertex_font_size': 32,
            'vertex_size': 64,
            'eorder': eorder,
            'edge_text': edge_text,
            'edge_color': edge_color,
            'edge_font_size': 64,
            'edge_text_distance': 8}


def core_update_setting(g, new_edge,
                        affected_nodes,
                        new_core_num,
                        edge_short_name=''):
    s = default_setting(g)
    for n in affected_nodes:
        s['vertex_fill_color'][n] = COLOR_BLUE

    e = g.edge(*new_edge)
    s['edge_color'][e] = COLOR_BLACK

    s['edge_text'][e] = edge_short_name
    s['eorder'][e] = 1
    return s
                                            

def house_pos(g):
    pos = g.new_vertex_property("vector<float>")
    pos[0] = (0.5, -1.75)
    pos[1] = (0, -1)
    pos[2] = (1, -1)
    pos[3] = (0, 0)
    pos[4] = (1, 0)
    pos[5] = (2, 0)

    meta_node_pos_dict = {
            'a': (0, 0),
            'b': (1, 0),
            'c,d,e': (0.5, 0.5),
    }
    
    return pos, meta_node_pos_dict


def example1_pos(g):
    pos = g.new_vertex_property('vector<float>')
    pos[0] = (0.5, -1)
    pos[1] = (0, 0)
    pos[2] = (1, 0)
    pos[3] = (2, -1)
    pos[4] = (3, -1)
    pos[5] = (2, 0)
    pos[6] = (3, 0)

    meta_node_pos_dict = {
            'a': (0, 0),
            'b': (1, 0),
            'c': (2, 0),
            'd': (1, 1),
            'e,f': (1, 2),
            'g': (2, 2)
    }
    return pos, meta_node_pos_dict


def get_method_styles():
    return [
        (COLOR_GREY, 'p', '-'),
        (COLOR_YELLOW, 's', '-'),
        (COLOR_PINK, '*', ':'),
        (COLOR_BLUE, '^', '--'),
        (COLOR_GREEN, 'v', '-.'),
        (COLOR_ORANGE, 'o', '-')
    ]
