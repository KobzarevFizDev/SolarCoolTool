from TimeDistancePlotBuilder.configuration import ConfigurationApp

c = ConfigurationApp("/home/changame/Programming/TimeDistancePlotBuilder/TimeDistancePlotBuilder/configuration.txt")
print("PATH " +  c.path_to_export_results)
print("PATH " + c.path_to_solar_images)

print("step_a94 " + str(c.step_for_channel_a94))
print("step_a131 " + str(c.step_for_channel_a131))
print("step_a171 " + str(c.step_for_channel_a171))
print("step_a193 " + str(c.step_for_channel_a193))
print("step_a211 " + str(c.step_for_channel_a211))
print("step_a304 " + str(c.step_for_channel_a304))
print("step_a335 " + str(c.step_for_channel_a335))


print("max_a94 " + str(c.max_number_of_frames_in_a94))
print("max_a131 " + str(c.max_number_of_frames_in_a131))
print("max_a171 " + str(c.max_number_of_frames_in_a171))
print("max_a193 " + str(c.max_number_of_frames_in_a193))
print("max_a211 " + str(c.max_number_of_frames_in_a211))
print("max_a304 " + str(c.max_number_of_frames_in_a304))
print("max_a335 " + str(c.max_number_of_frames_in_a335))


