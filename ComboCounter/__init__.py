import unrealsdk
import datetime

from ..ModMenu import EnabledSaveType, SDKMod


class ComboCounter(SDKMod):
	Name: str = "Kill Combo Counter"
	Description: str = "Adds a Kill Combo Counter to your screen.\nAfter 6 seconds of no killing the combo will vanish.\nThe higher the Combo the more additional exp you gain on kill."
	Author: str = "Juso"
	Version: str = "1.0"
	SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadOnMainMenu
	
	_started_at = datetime.datetime.utcnow()
	KillCounter = 0
	#This is our timer function it gets called with the Instance of this class. In this case its ComboInstance()
	def __call__(self):
		time_passed = datetime.datetime.utcnow() - self._started_at
		#If 6 seconds are up, then reset the Kill Counter
		if time_passed.total_seconds() > 6:
			self.KillCounter = 0
			return False
		return True

	#Returns the current WillowPlayerController
	def GetPlayerController(self):
		return unrealsdk.GetEngine().GamePlayers[0].Actor

	def ComboFeedback(self, EnemyName):
		ComboNames = [
				"First Blood",
				"Double Kill",
				"Triple Kill",
				"Overkill",
				"Multi Kill",
				"Monster Kill",
				"Ultra Kill",
				"Killing Spree",
				"Killtrocity",
				"Killamanjaro",
				"Killtastrophe",
				"Killpocalypse",
				"Godlike",
				"Unstoppable!",
				"Unfriggenbelievable"
				]
		if self.KillCounter < len(ComboNames)+1:
			ComboName = ComboNames[self.KillCounter-1]
		else:
			ComboName = ComboNames[-1]
		#This gets the Players HUD
		playerController = self.GetPlayerController()
		HUDMovie = playerController.GetHUDMovie()
		#This is the Title of the Combo Counter
		KillString = str(self.KillCounter) + " Kills\n\nLast Killed Enemy: " + EnemyName
		#This First clears the old message and then rewrites the new one
		HUDMovie.ClearTrainingText()
		HUDMovie.AddTrainingText(KillString, ComboName, 6.000000, (), "", False, 0, playerController.PlayerReplicationInfo, True)
		
	#We reset our timer
	#then increase the kill counter by one, because a kill happened
	def KillCombo(self, caller, function, params):
		self._started_at = datetime.datetime.utcnow()
		self.KillCounter+=1
		max_multiplier = 15
		#Optional Extra Experience
		if self.KillCounter <= max_multiplier: #Change to whatever kill xp multiplier you want to
			unrealsdk.GetEngine().GamePlayers[0].Actor.ExpEarn(int(self.KillCounter**2.8),0)
		else:
			unrealsdk.GetEngine().GamePlayers[0].Actor.ExpEarn(int(max_multiplier**2.8),0)
		self.ComboFeedback(params.EnemyName)
		return True
		
	KillHook = "WillowGame.WillowPlayerController.NotifyKilledEnemy"
	def Enable(self):
		unrealsdk.RegisterHook(self.KillHook, "KillHook", KillComboHook)
	def Disable(self):
		unrealsdk.RemoveHook(self.KillHook, "KillHook")

ComboInstance = ComboCounter()

def KillComboHook(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
	ComboInstance()
	ComboInstance.KillCombo(caller, function, params)
	return True

unrealsdk.RegisterMod(ComboInstance)
