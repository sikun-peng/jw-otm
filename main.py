import wx
from gui import MyFrame
from process import process_csv

app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()

a_to_z_csv_path = frame.get_a_to_z_csv_path()
enable_homestead_check = frame.get_enable_homestead_check()
enable_voter_registration_check = frame.get_enable_voter_registration_check()
voter_registration_csv_path = frame.get_voter_registration_csv_path()
enable_use_otm_file = frame.get_enable_use_otm_file()
otm_csv_path = frame.get_otm_csv_path()
output_path = frame.get_output_path()
output_file_name = frame.get_output_file_name()

process_csv(a_to_z_csv_path, 
	enable_homestead_check, 
	enable_voter_registration_check,
	voter_registration_csv_path,
	enable_use_otm_file,
	otm_csv_path,
	output_path,
	output_file_name)