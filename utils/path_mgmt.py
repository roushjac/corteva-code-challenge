def add_corteva_to_path():
    # using a little hack to allow the corteva_app module to be seen in this module
    import sys
    sys.path.insert(0, "..")