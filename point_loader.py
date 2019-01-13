#!/usr/bin/env python3
import yaml
import point

def load_yaml_points(control, filename):
    with open(filename, 'r') as s:
        struct = yaml.load(s)
        for p in struct['points']:
            name = p["point"]["name"]
            left_url = p["point"]["left_url"]
            left_img = p["point"]["left_img"]
            right_url = p["point"]["right_url"]
            right_img = p["point"]["right_img"]
            new_point = point.point(name, left_url, left_img, right_url, right_img)
            control.add_point(new_point)
        uri_on_1 = struct['rails']['uri_on_1']
        uri_on_2 = struct['rails']['uri_on_2']
        uri_off_1 = struct['rails']['uri_off_1']
        uri_off_2 = struct['rails']['uri_off_2']
        control.add_rail_uris(uri_on_1, uri_on_2, uri_off_1, uri_off_2)

if __name__ == "__main__":
    import controller
    c = controller.controller()
    load_yaml_points(c, "points.yaml")
    a = [(p.get_name(), p.get_left_url(), p.get_left_img(), p.get_right_url(), p.get_right_img()) for p in c.get_points()]
    print(str(a))
