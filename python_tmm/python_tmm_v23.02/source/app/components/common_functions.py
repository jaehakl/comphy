def bind_state(model, setModel):
    if model is not None:
        module_cls = model[0]
        model_id = model[1]
        if len(model) > 2:
            data_index = model[2]
        else:
            data_index = None
        module_cls().bind(model_id, id, setModel, data_index)