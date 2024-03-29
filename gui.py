import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Data Processing Tool', size=(600, 450))  # Default size increased by 30%
        panel = wx.Panel(self)
        
        # File selector for A_TO_Z_CSV_PATH
        file_label_a_to_z = wx.StaticText(panel, label="Select A_TO_Z CSV file:")
        self.file_picker_a_to_z = wx.FilePickerCtrl(panel, wildcard="CSV files (*.csv)|*.csv")
        self.file_picker_a_to_z.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_fields_changed)
        
        # Checkbox for ENABLE_HOMESTEAD_CHECK
        self.enable_homestead_check = wx.CheckBox(panel, label="Enable Homestead Check")
        self.enable_homestead_check.SetValue(False)  # Default: unchecked
        self.enable_homestead_check.Bind(wx.EVT_CHECKBOX, self.on_fields_changed)
        
        # Checkbox for ENABLE_VOTER_REGISTRATION_CHECK
        self.enable_voter_registration_check = wx.CheckBox(panel, label="Enable Voter Registration Check")
        self.enable_voter_registration_check.SetValue(False)  # Default: unchecked
        self.enable_voter_registration_check.Bind(wx.EVT_CHECKBOX, self.on_voter_registration_checkbox)
        
        # File selector for VOTER_REGISTRATION_CSV_PATH
        file_label_voter_registration = wx.StaticText(panel, label="Select Voter Registration CSV file:")
        self.file_picker_voter_registration = wx.FilePickerCtrl(panel, wildcard="CSV files (*.csv)|*.csv")
        self.file_picker_voter_registration.Disable()  # Initially disabled
        self.file_picker_voter_registration.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_fields_changed)

        # Checkbox for ENABLE_USE_OTM_FILE
        self.enable_use_otm_file = wx.CheckBox(panel, label="Enable Use of OTM File")
        self.enable_use_otm_file.SetValue(False)  # Default: unchecked
        self.enable_use_otm_file.Bind(wx.EVT_CHECKBOX, self.on_use_otm_file_checkbox)

        # File selector for OTM_CSV_PATH
        file_label_otm = wx.StaticText(panel, label="Select OTM CSV file:")
        self.file_picker_otm = wx.FilePickerCtrl(panel, wildcard="CSV files (*.csv)|*.csv")
        self.file_picker_otm.Disable()  # Initially disabled
        self.file_picker_otm.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_fields_changed)
        
        # Text input for output file name
        output_label = wx.StaticText(panel, label="Output File Name:")
        self.output_file_input = wx.TextCtrl(panel, value="output", style=wx.TE_PROCESS_ENTER)
        self.output_file_postfix = wx.StaticText(panel, label=".csv")
        self.output_file_input.Bind(wx.EVT_TEXT_ENTER, self.on_fields_changed)
        self.output_file_input.Bind(wx.EVT_TEXT, self.on_fields_changed)
        
        # Button to select output folder
        output_folder_label = wx.StaticText(panel, label="Select Output Folder:")
        self.output_picker = wx.DirPickerCtrl(panel, style=wx.DIRP_USE_TEXTCTRL)
        self.output_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_fields_changed)
        
        # Button to start processing
        self.start_button = wx.Button(panel, label="Start Processing")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.start_button.Disable()  # Initially disabled
        
        # Layout
        output_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_sizer.Add(self.output_file_input, 1, wx.EXPAND|wx.ALL, 5)
        output_sizer.Add(self.output_file_postfix, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(file_label_a_to_z, 0, wx.ALL, 5)
        sizer.Add(self.file_picker_a_to_z, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.enable_homestead_check, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.enable_voter_registration_check, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(file_label_voter_registration, 0, wx.ALL, 5)
        sizer.Add(self.file_picker_voter_registration, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.enable_use_otm_file, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(file_label_otm, 0, wx.ALL, 5)
        sizer.Add(self.file_picker_otm, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(output_label, 0, wx.ALL, 5)
        sizer.Add(output_sizer, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(output_folder_label, 0, wx.ALL, 5)
        sizer.Add(self.output_picker, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.start_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        panel.SetSizer(sizer)
        
    def on_start(self, event):
        self.a_to_z_csv_path = self.file_picker_a_to_z.GetPath()
        self.enable_homestead_check = self.enable_homestead_check.GetValue()
        self.enable_voter_registration_check = self.enable_voter_registration_check.GetValue()
        self.enable_use_otm_file = self.enable_use_otm_file.GetValue()
        self.voter_registration_csv_path = self.file_picker_voter_registration.GetPath() if self.enable_voter_registration_check else None
        self.otm_csv_path = self.file_picker_otm.GetPath() if self.enable_use_otm_file else None
        self.output_path = self.output_picker.GetPath()
        self.output_file_name = self.output_file_input.GetValue() + ".csv"
        self.Close()

    def on_voter_registration_checkbox(self, event):
        if self.enable_voter_registration_check.GetValue():
            self.file_picker_voter_registration.Enable()
        else:
            self.file_picker_voter_registration.Disable()
        self.on_fields_changed(event)  # Trigger fields changed event

    def on_use_otm_file_checkbox(self, event):
        if self.enable_use_otm_file.GetValue():
            self.file_picker_otm.Enable()
        else:
            self.file_picker_otm.Disable()
        self.on_fields_changed(event)  # Trigger fields changed event
    
    def on_fields_changed(self, event):
        a_to_z_path = self.file_picker_a_to_z.GetPath()
        output_path = self.output_picker.GetPath()
        output_name = self.output_file_input.GetValue()
        if a_to_z_path and output_path and output_name:
            self.start_button.Enable()
        else:
            self.start_button.Disable()
    
    def get_a_to_z_csv_path(self):
        return self.a_to_z_csv_path
    
    def get_enable_homestead_check(self):
        return self.enable_homestead_check
    
    def get_enable_voter_registration_check(self):
        return self.enable_voter_registration_check
    
    def get_enable_use_otm_file(self):
        return self.enable_use_otm_file
    
    def get_voter_registration_csv_path(self):
        return self.voter_registration_csv_path
    
    def get_otm_csv_path(self):
        return self.otm_csv_path
    
    def get_output_path(self):
        return self.output_path
    
    def get_output_file_name(self):
        return self.output_file_name

