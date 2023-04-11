import arrow
import networkx
import networkx as nx
import skyfield.api

from sat.tool.distance_tools import get_distance_between_two_sat


def create_topo(sat_dict, gs_list, t:skyfield.api.Time) -> networkx.Graph:
    print(f'{arrow.now().isoformat()}  开始生成图: {t.utc_iso()}')
    G = nx.Graph()
    G.add_nodes_from(sat_dict.values())
    G.add_nodes_from(gs_list)

    for sat in sat_dict.values():
        forward, back = sat.get_intra_sats(t)
        if forward is not None and back is not None:
            forward_sat = sat_dict[forward]
            back_sat = sat_dict[back]
            G.add_edge(sat, forward_sat, weight=get_distance_between_two_sat(sat, forward_sat, t))
            G.add_edge(sat, back_sat, weight=get_distance_between_two_sat(sat, back_sat, t))

        left, right = sat.get_extra_sats(t)
        if left != '0_0' and right != '0_0':
            left_sat = sat_dict[left]
            right_sat = sat_dict[right]
            G.add_edge(sat, left_sat, weight=get_distance_between_two_sat(sat, left_sat, t))
            G.add_edge(sat, right_sat, weight=get_distance_between_two_sat(sat, right_sat, t))

    for gs in gs_list:
        linked_sat_dict = gs.get_link_sat(t)
        if linked_sat_dict is None:
            continue
        linked_sat = sat_dict[linked_sat_dict[1]]
        distance = linked_sat_dict[0]
        G.add_edge(gs, linked_sat, weight=distance)

    return G