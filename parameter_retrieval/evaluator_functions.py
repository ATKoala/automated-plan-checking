import strings

def _evaluate_gantry(param_value, table_value, **kwargs):
    # This line checks whether the parameter value found is the same as the truth table value (this is why the formating of the two dictionaries is important) and gives a "PASS" value
    # Also there are other instances where a PASS is given such as if the Truth Table is a dash for a given parameter in that case any value will satisfy
    # Or if the file is a VMAT and the parameter is either a gantry or an SSD
    file_type = kwargs["file_type"]

    for value in table_value.split(","):
        if not value.isdigit() and value!=strings.ANY_VALUE:
            return strings.TRUTH_TABLE_ERROR

    if file_type == strings.VMAT:
        return strings.PASS
    else:
        return strings.PASS if (param_value == table_value or table_value == strings.ANY_VALUE) else strings.FAIL

def _evaluate_ssd(param_value, table_value, **kwargs):
    if table_value == strings.ANY_VALUE:
        return strings.PASS

    for value in table_value.split(","):
        if not value.isdigit() and value!=strings.ANY_VALUE and value!="?":
            return strings.TRUTH_TABLE_ERROR

    if kwargs["file_type"] == strings.VMAT:
        truth_table = kwargs["truth_table"]
        parameter_values = kwargs["parameter_values"]
        case = kwargs["case"]

        if truth_table[strings.gantry][case-1] == strings.ANY_VALUE or parameter_values[strings.gantry] == "error retrieving gantry":
            if truth_table[strings.gantry][case-1] != strings.ANY_VALUE:
                return strings.PASS
            else:
                return strings.FAIL

        if len(parameter_values[strings.gantry])!=len(parameter_values[strings.SSD]):
            return strings.FAIL

        truth_table_gantry_list = truth_table[strings.gantry][case-1].split(',')
        truth_table_ssd_list = truth_table[strings.SSD][case-1].split(',')
        if len(truth_table_gantry_list) != len(truth_table_ssd_list):
            return strings.FAIL

        for i in range(len(truth_table_gantry_list)):
            gantry_value = float(truth_table_gantry_list[i])
            ssd_value = truth_table_ssd_list[i]
            if ssd_value == '?':
                continue

            ssd_value=float(ssd_value)
            j = 0
            while j < len(parameter_values[strings.gantry]):
                if abs(parameter_values[strings.gantry][j] - gantry_value) < 0.3:
                    if abs(parameter_values[strings.SSD][j] - ssd_value) > 1:
                        return strings.FAIL
                j+=1
        return strings.PASS
    else:
        truth_table_ssd_list = table_value.split(',')
        if len(truth_table_ssd_list) != len(param_value):
            return strings.FAIL

        i=0
        while i < len(truth_table_ssd_list):
            if truth_table_ssd_list[i] != '?':
                if abs(int(truth_table_ssd_list[i])-float(param_value[i])) > 1:
                    return strings.FAIL
            i+=1
        return strings.PASS


def _evaluate_wedge(param_value, table_value, **kwargs):

    for value in table_value.split(","):
        if not value.isdigit() and value!=strings.ANY_VALUE and value!="no wedge":
            return strings.TRUTH_TABLE_ERROR

    if table_value == 'no wedge':
        all_no_wedge = all(map(lambda w_angle: w_angle == 'no wedge', param_value.split(',')))
        return strings.PASS if all_no_wedge else strings.FAIL
    else:
        return strings.PASS if table_value == param_value else strings.FAIL

def _evaluate_prescription_dose(param_value, table_value, **kwargs):
    for i in range(0, 3):
        if table_value.split("/")[i] != strings.ANY_VALUE and table_value.split("/")[i] != param_value.split("/")[i]:
            return strings.FAIL
    return strings.PASS

def _evaluate_collimator(param_value, table_value, **kwargs):

    for value in table_value.split(","):
        if not value.isdigit() and value!=strings.ANY_VALUE:
            if not value[0] == "*" or len(value)<2 or not value[1:].isdigit():
                return strings.TRUTH_TABLE_ERROR

    if table_value == strings.ANY_VALUE:
        return strings.PASS

    result = table_value == param_value if table_value[0] != '*' else    \
             table_value[1:] != param_value
    return strings.PASS if result else strings.FAIL

def _evaluate_energy(param_value, table_value, **kwargs):
    if param_value in ["6","6FFF","10","10FFF","18"]:
        return "N/A"
    else:
        return "N/A"

def _evaluate_field_size(param_value, table_value, **kwargs):
    if param_value =="Not Extracted":
        return "NOT IMPLEMENTED FOR MLCX/MLCY"
    else:
        if table_value == '-':
            return strings.PASS
        else:
            truth_table_ssd_list = table_value.split(',')
            i = 0
            for i in range(len(truth_table_ssd_list)):
                if truth_table_ssd_list[i] != '?':
                    if param_value == truth_table_ssd_list[i]:
                        return strings.PASS
            return strings.FAIL


def _evaluate_default(param_value, table_value, **kwargs):
    return strings.PASS if param_value == table_value or table_value == '-' else strings.FAIL

evaluator_functions = {
    strings.mode_req                : _evaluate_default,
    strings.prescription_dose_slash_fractions    : _evaluate_prescription_dose,
    strings.prescription_point      : _evaluate_default,
    strings.isocenter_point         : _evaluate_default,
    strings.override                : _evaluate_default,
    strings.collimator              : _evaluate_collimator,
    strings.gantry                  : _evaluate_gantry,
    strings.SSD                     : _evaluate_ssd,
    strings.couch                   : _evaluate_default,
    strings.field_size              : _evaluate_field_size,
    strings.wedge                   : _evaluate_wedge,
    strings.meas                    : _evaluate_default,
    strings.energy                  : _evaluate_energy,
}
