import events
import re


def invert_main():
    mer_file_path = "tool_invert_mer/"
    mevents = events.Events(mer_file_path)
    for event in mevents.events:
        print event.file_name
        with open(mer_file_path + event.file_name, 'r') as f:
            content = f.read()
        environment = re.findall("<ENVIRONMENT>.+</PARAMETERS>", content, re.DOTALL)[0]
        event.set_environment(environment)
        event.find_measured_sampling_frequency()
        event.correct_date()
        event.invert_transform()
        event.plotly(mer_file_path)
        event.plot(mer_file_path)
        event.to_sac_and_mseed(mer_file_path, station_number="00", force_without_loc=True)


if __name__ == "__main__":
    invert_main()
