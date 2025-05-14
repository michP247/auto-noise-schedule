import modules.scripts as scripts
import modules.shared as shared
from modules.script_callbacks import on_model_loaded

DEBUG_PRINT = True

V_PREDICTION_SCHEDULE = "Zero Terminal SNR"
EPSILON_PREDICTION_SCHEDULE = "Default"
TARGET_OPTION_NAME = "sd_noise_schedule"

def on_model_loaded_callback(sd_model):
    if sd_model is None:
        if DEBUG_PRINT: print("[AutoNoiseSchedule] No model loaded.")
        return

    if not hasattr(shared.opts, TARGET_OPTION_NAME):
        if DEBUG_PRINT: print(f"[AutoNoiseSchedule] Option '{TARGET_OPTION_NAME}' not found.")
        return

    model_name = "Unknown Model"
    sd_checkpoint_info = getattr(sd_model, 'sd_checkpoint_info', None)
    if sd_checkpoint_info and hasattr(sd_checkpoint_info, 'name') and sd_checkpoint_info.name:
        model_name = sd_checkpoint_info.name
    elif hasattr(sd_model, 'filename') and sd_model.filename:
        model_name = sd_model.filename

    prediction_type_from_kmodel_predictor = None
    
    forge_objects = getattr(sd_model, 'forge_objects', None)
    if not forge_objects:
        if DEBUG_PRINT: print("[AutoNoiseSchedule] sd_model.forge_objects not found.")
    else:
        unet_patcher = getattr(forge_objects, 'unet', None)
        if not unet_patcher:
            if DEBUG_PRINT: print("[AutoNoiseSchedule] sd_model.forge_objects.unet (UnetPatcher) not found.")
        else:
            k_model_instance = getattr(unet_patcher, 'model', None) 
            if not k_model_instance:
                if DEBUG_PRINT: print("[AutoNoiseSchedule] unet_patcher.model (KModel instance) not found.")
            else:
                predictor_object = getattr(k_model_instance, 'predictor', None)
                if not predictor_object:
                    if DEBUG_PRINT: print("[AutoNoiseSchedule] KModel.predictor object not found.")
                else:
                    p_type_attr = getattr(predictor_object, 'prediction_type', None)
                    if p_type_attr is not None:
                        prediction_type_from_kmodel_predictor = p_type_attr
                    elif DEBUG_PRINT:
                        print("[AutoNoiseSchedule] KModel.predictor does not have 'prediction_type' attribute or it's None.")

    current_schedule = shared.opts.data.get(TARGET_OPTION_NAME, None)
    new_schedule = None

    if prediction_type_from_kmodel_predictor:
        if prediction_type_from_kmodel_predictor == 'v_prediction':
            new_schedule = V_PREDICTION_SCHEDULE
            if DEBUG_PRINT: print(f"[AutoNoiseSchedule] v_prediction type detected from KModel.predictor for '{model_name}'.")
        else: 
            new_schedule = EPSILON_PREDICTION_SCHEDULE
            if DEBUG_PRINT: print(f"[AutoNoiseSchedule] Non-v_prediction type ('{prediction_type_from_kmodel_predictor}') detected from KModel.predictor for '{model_name}'.")
    else:
        new_schedule = EPSILON_PREDICTION_SCHEDULE # Default if type couldn't be determined
        if DEBUG_PRINT: print(f"[AutoNoiseSchedule] Could not determine prediction_type from KModel.predictor for '{model_name}'. Defaulting to Epsilon schedule.")

    if new_schedule and current_schedule != new_schedule:
        shared.opts.set(TARGET_OPTION_NAME, new_schedule)
        if DEBUG_PRINT: print(f"[AutoNoiseSchedule] Changed '{TARGET_OPTION_NAME}' from '{current_schedule}' to '{new_schedule}'.")
    elif DEBUG_PRINT:
        if new_schedule: print(f"[AutoNoiseSchedule] '{TARGET_OPTION_NAME}' is already set to '{new_schedule}'.")

on_model_loaded(on_model_loaded_callback)

if DEBUG_PRINT:
    print("[AutoNoiseSchedule] Extension loaded.")

class AutoNoiseScheduleScript(scripts.Script):
    def title(self):
        return "Automatic Noise Schedule"