from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.boxlayout import BoxLayout
import pickle
import os
import threading
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from SyncsFoldersV1 import chType, SyncFolders

Builder.load_file(r"c:\Users\saban\Desktop\TKINTER\X_tkinter\Syncs.kv")


class ShowListOfSub(BoxLayout):
    def __init__(self, _listSub, **k):
        super().__init__(**k)
        x = 0
        for i in AppV1_1().AllSubDirs:
            x += 1
            print(i)
            self.ids.AllDirectories.add_widget(OneLineListItem(text=f"hello"))


class AppV1_1(Widget):

    def __init__(self, **kwargs):
        super(AppV1_1, self).__init__(**kwargs)
        self.IsAction = None  # need do something
        self.SyncFolder = SyncFolders()
        self.ALERT = None
        self.SeeListSub = None
        self.RootDir = None
        self.ids.PathMainDir.hint_text = fr"C:\Users\{self.SyncFolder.Name}:"
        self.FM = rf"c:\Users\{self.SyncFolder.Name}\AppSyncs"
        self.SMNF = rf"{self.FM}\SMNF"
        self.AllSubDirs = []
        self.NumFolders = 0
        self.NumFiles = 0
        self.__call__()

    def __call__(self, *args, **kwargs):
        self.Memory()
        if self.CheckMemory(flag="Main"):
            self.RootDir = self.LetMainDir()
            self.ids.StartSyncs.text = f"START SYNCS WITH {self.RootDir}"
            MB = self.ids.SaveMainDir
            MT = self.ids.PathMainDir
            MB.text = "Change"
            MT.text = self.RootDir
            self.CheckMemory(flag="Sub")

    def PathOfMainDir(self):
        Path = self.ids.PathMainDir

        if "c:" in Path.text.lower():
            if self.CheckPath(Path.text):
                self.ids.SaveMainDir.text = "Change"
                self.RootDir = Path.text
                OFile = open(self.SMNF, "rb")
                data = pickle.load(OFile)
                OFile.close()
                data.update({'Main': Path.text})
                OFile = open(self.SMNF, "wb")
                pickle.dump(data, OFile)
                OFile.close()
                self.AlertErrorPath("Succeeded", "Path Saved!")
                self.ids.StartSyncs.text = f"START SYNCS WITH {Path.text}"

            else:
                self.AlertErrorPath("Path Not Found", "Your Path Not Exist or this path is File!")

        else:
            self.AlertErrorPath("Path Not Found", "Enter Path!")

    def OpenAllSubDirectories(self):
        if not self.SeeListSub:
            self.SeeListSub = MDDialog(
                title="SUB FOLDERS:",
                type="custom",
                content_cls=ShowListOfSub(self.AllSubDirs),
                buttons=[MDFlatButton(
                    text="Close",
                    on_press=self.CloseListSub
                )]
            )

        self.SeeListSub.open()

    def CloseListSub(self, *args):
        try:
            self.SeeListSub.dismiss(force=True)
        except AttributeError:
            pass

    def AlertErrorPath(self, Tit, Tex):
        if not self.ALERT:
            self.ALERT = MDDialog(
                title=Tit,
                text=f"———— {Tex} ————",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_press=self.CloseAlert)],
            )
        self.ALERT.open()
        self.ALERT = None

    def CloseAlert(self, *args):
        try:
            self.ALERT.dismiss(force=True)
        except AttributeError:
            pass

    def OptionsOfSubDirs(self):
        BottomSM = MDGridBottomSheet()
        data = [
            {"text": "Delete All Sub", 'func': self.DelSubMemory, "ico": "delete-forever"},
            {"text": "Append Folder", 'func': self.SaveSubDirectories, "ico": "plus-box-outline"},
            {"text": 'open list sub', 'func': self.OpenAllSubDirectories, "ico": "open-in-new"}
        ]
        for _dict in data:
            BottomSM.add_item(
                _dict['text'].upper(),
                lambda _none, _function=_dict['func']: _function(),
                icon_src=_dict['ico'])

        BottomSM.open()

    def LetMainDir(self):
        OFile = open(self.SMNF, "rb")
        data = pickle.load(OFile)
        OFile.close()
        return data['Main']

    def Memory(self, WD=None):  # -> list

        # by if
        if not os.path.exists(self.FM):
            os.mkdir(self.FM)

        if not len(os.listdir(self.FM)) == 1 and not WD:
            OFile = open(self.SMNF, "ab")
            pickle.dump({"Main": None, "Sub1": None}, OFile)

        elif WD:
            os.system(f"del {self.SMNF}")
            OFile = open(self.SMNF, "ab")
            pickle.dump({"Main": WD[0], "Sub1": None}, OFile)

            # end
            OFile.close()

    def DelSubMemory(self):
        x = []
        if os.path.exists(self.FM):

            # take 1.Main 2.numFile 3.numFolder
            OFile = open(self.SMNF, "rb")
            data = pickle.load(OFile)
            OFile.close()
            x.append(data['Main'])
            self.Memory(WD=x)
            self.AllSubDirs = []
            self.CheckMemory(flag="Sub")

    # bool-> *
    def CheckMemory(self, flag='Main'):
        OFile = open(self.SMNF, "rb")
        data = pickle.load(OFile)
        OFile.close()

        if flag == "Main":
            if data["Main"]:
                return True
            else:
                return False
        if flag == "Sub":
            for k, v in data.items():
                if "Sub" in k:
                    print(k, v)
                    self.AllSubDirs.append(v)

    def SaveSubDirectories(self):

        obj2 = self.ids.Dir1

        OFile = open(self.SMNF, "rb")
        data = pickle.load(OFile)
        OFile.close()

        # CHECK
        x_check = []
        for path in data.values():
            x_check.append(path)

        if self.CheckPath(obj2.text) and obj2.text != data['Main'] and obj2.text not in x_check and self.RootDir:
            self.AllSubDirs.append(obj2.text)
            OFile = open(self.SMNF, "wb")
            data[f'Sub{len(data.keys())}'] = obj2.text
            print(f'Sub{len(data.keys())}')
            pickle.dump(data, OFile)
            OFile.close()
            obj2.text = ""
            self.AlertErrorPath("Succeeded", "path Append to Lists Of folders !")

        else:
            self.AlertErrorPath("Have some Errors",
                                "check Your path\n\n | maybe this path already exist! or is Your Main Directory!\n\n"
                                "| or Maybe Main Dir isn't define!")

    def AllFilesFolders(self):

        OFile = open(self.SMNF, "rb")
        data = pickle.load(OFile)
        OFile.close()

        # need a lot power from CPU \:
        if not data['NumFile']:
            os.chdir("c:\\")
            self.ids.WindowMenu.title = f"scanning....c:\\*"
            for PATH in os.popen("dir /s /b *").read().split("\n"):
                if chType(PATH):
                    self.NumFiles += 1
                else:
                    self.NumFolders += 1

                self.ids.WindowMenu.title = f"Have {self.NumFolders:,} Folders in Computer and {self.NumFiles:,} files"

            data.update({'NumFile': self.NumFiles, 'NumFolder': self.NumFolders})
            OFile = open(self.SMNF, "wb")
            pickle.dump(data, OFile)
            OFile.close()
        else:
            OFile = open(self.SMNF, "rb")
            data = pickle.load(OFile)
            OFile.close()
            self.ids.WindowMenu.title = \
                f"Have {int(data['NumFolder']):,} Folders in Computer and {int(data['NumFile']):,} files"

    def OpenStartSyncs(self):
        threading.Thread(target=self.StartSyncs).start()

    def StartSyncs(self):
        if self.RootDir and len(self.AllSubDirs) >= 1 and type(self.IsAction) is bool:
            x = 0
            self.ids.StartSyncs.disabled = True
            for SubFolder in self.AllSubDirs:
                x += 1
                self.ids.WindowMenu.title = \
                    f"Mapping Folder..{SubFolder} {(x * 100) // (len(self.AllSubDirs))}% complete"
                if SubFolder:
                    if os.path.exists(SubFolder):
                        self.SyncFolder.Sync(self.SyncFolder.GetFolders(self.RootDir, SubFolder), RSL=self.IsAction)
                else:
                    self.AlertErrorPath("Folder Not Found", f"{SubFolder} Not Found!")
            self.ids.StartSyncs.disabled = False

            info = self.SyncFolder.Info().split("|")
            self.ids.WindowMenu.title = \
                f"Finite Syncs! -> {info[0]} Files Checking  {info[1]} folders -*- {info[2]} Files Syncs"

        else:
            self.AlertErrorPath("Have Error!", "You need define at least 1 sub dir "
                                               "{required main folder!}\n AND define MODE!")

    def SelectMode(self, Check, true):
        if Check == self.ids.ModeMain:
            self.ids.ModeSub.disabled = true
            self.IsAction = true
        else:
            self.ids.ModeMain.disabled = true
            self.IsAction = False

        if not true:
            self.IsAction = None

    # Bool ->
    @staticmethod
    def CheckPath(path):
        if "c:" in path.lower():
            if os.path.exists(path) and not chType(path):
                return True
            else:
                return False

        else:
            return False


class FileSynchronization(MDApp):

    def build(self):
        return AppV1_1()


FileSynchronization().run()
