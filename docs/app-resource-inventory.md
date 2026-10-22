# App resource implementation inventory

I compared the local MyBuderus 5.0.0 resource models with v0.8.2-beta.4.
This index records path definitions, including composed heating and hot-water
paths. It does not equate an APK reference with a working device capability.
No APK files, bytecode, demo data, credentials or device values are included.

The complete machine-readable index is [app-resource-inventory.json](app-resource-inventory.json).
Each entry keeps the device adapter, model name, path or unresolved fragment,
implementation status, intended HA mapping and outstanding metadata evidence.

| Status | Resource model definitions |
|---|---:|
| Excluded: private or administrative | 31 |
| Existing curated path; live schema still required | 247 |
| Implemented read contract, device verification pending | 11 |
| Not released; semantics or adapter review pending | 34 |
| Optional history, not implemented | 11 |
| Structured format needs parser and device fixture | 18 |
| Unresolved path composition | 7 |

Multiple app models may refer to the same resource. The number of model
definitions is not an entity count. Resource types, units, bounds and command
semantics must still be reviewed per unresolved entry. The inventory is a
checkpoint for package 1, not its final acceptance.

| Adapter | Resource model | Path or fragment | Status |
|---|---|---|---|
| connectkeyprovider | `ConnectKeyConfiguringResource$UpdateTriggerRequest` | `/gateway/update/triggerRequest` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyDevicesResource$ActualHumidity` | `/devices/device/actualHumidity` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$DevicesList` | `/devices/list` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$Errors` | `/devices/device/errors` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$InclusionTime` | `/devices/inclusionTime` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$InclusionWhiteList` | `/devices/inclusionWhitelist` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$RfTimeOfConnectionLost` | `/devices/device/rfTimeofConnectionLost` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$RoomTemperature` | `/devices/device/roomtemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDevicesResource$VersionFirmware` | `/devices/device/versionFirmware` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$Dhw1ReduceTempOnAlarm` | `/dhwCircuits/{dhw}/reduceTempOnAlarm` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwActualTemperature` | `/dhwCircuits/{dhw}/actualTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwCharge` | `/dhwCircuits/{dhw}/charge` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwChargeDuration` | `/dhwCircuits/{dhw}/chargeDuration` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwChargeRemainingTime` | `/dhwCircuits/{dhw}/chargeRemainingTime` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwCurrentFriwaSupplyTemperature` | `/dhwCircuits/{dhw}/currentFriwaSupplyTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwCurrentSetpoint` | `/dhwCircuits/{dhw}/currentSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwCurrentTemperatureLevel` | `/dhwCircuits/{dhw}/currentTemperatureLevel` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwFriwaPrimaryPumpModulation` | `/dhwCircuits/{dhw}/friwaPrimaryPumpModulation` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwName` | `/dhwCircuits/{dhw}/name` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwOperationMode` | `/dhwCircuits/{dhw}/operationMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwOutTemp` | `/dhwCircuits/{dhw}/outTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwSingleChargeSetpoint` | `/dhwCircuits/{dhw}/singleChargeSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwSwitchProgramA` | `/dhwCircuits/{dhw}/switchPrograms/A` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwTemperatureLevels` | `/dhwCircuits/{dhw}/temperatureLevels` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwTemperatureLevelsEco` | `/dhwCircuits/{dhw}/temperatureLevels/eco` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwTemperatureLevelsHigh` | `/dhwCircuits/{dhw}/temperatureLevels/high` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwTemperatureLevelsLow` | `/dhwCircuits/{dhw}/temperatureLevels/low` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwTemperatureLevelsOff` | `/dhwCircuits/{dhw}/temperatureLevels/off` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwType` | `/dhwCircuits/{dhw}/dhwType` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$DhwVolumeFlow` | `/dhwCircuits/{dhw}/volumeFlow` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyDhwCircuitResource$OverallStatus` | `/dhwCircuits/{dhw}/overallStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyGatewayResource$DataProcessingStatus` | `/gateway/dataProcessing/status` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyGatewayResource$DateTime` | `/gateway/dateTime` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$EthIpv4` | `/gateway/eth/ip/ipv4` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$EthIpv6` | `/gateway/eth/ip/ipv6` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$EthMac` | `/gateway/eth/mac` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$SerialId` | `/gateway/serialId` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$Uuid` | `/gateway/uuid` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$VersionFirmware` | `/gateway/versionFirmware` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyGatewayResource$VersionHardware` | `/gateway/versionHardware` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyGatewayResource$WifiIpv4` | `/gateway/wifi/ip/ipv4` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$WifiIpv6` | `/gateway/wifi/ip/ipv6` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$WifiMac` | `/gateway/wifi/mac` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyGatewayResource$WifiSsid` | `/gateway/wifi/ssid` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$ActualHeatDemand` | `/heatSources/actualHeatDemand` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$ActualModulation` | `/heatSources/actualModulation` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$ActualSupplyTemperature` | `/heatSources/actualSupplyTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$AdditionalHeater$OperationMode` | `/heatSources/additionalHeater/operationMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$BrineCircuit$CollectorInflowTemp` | `/heatSources/{hs}/brineCircuit/collectorInflowTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$BrineCircuit$CollectorOutflowTemp` | `/heatSources/{hs}/brineCircuit/collectorOutflowTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$CHStatus` | `/heatSources/chStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$CompressorStatus` | `/heatSources/compressor/status` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$CurrentEmergencyMode` | `/heatSources/currentEmergencyMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$DefrostActive` | `/heatSources/{hs}/defrostActive` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EHeaterStatus` | `/heatSources/Source/eHeater/status` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EmStatus` | `/heatSources/emStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EmonLifetime$ChConsumption` | `/heatSources/emon/chConsumption` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EmonLifetime$CoolingConsumption` | `/heatSources/emon/coolingConsumption` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EmonLifetime$DhwConsumption` | `/heatSources/emon/dhwConsumption` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EmonLifetime$PoolConsumption` | `/heatSources/emon/poolConsumption` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$EmonLifetime$TotalConsumption` | `/heatSources/emon/totalConsumption` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$HPType` | `/heatSources/{hs}/heatPumpType` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$ActiveHeatSource` | `/heatSources/hybrid/activeHeatSource` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$ControlStrategy` | `/heatSources/hybrid/controlStrategy` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$OutdoorStatus` | `/heatSources/hybrid/outdoorStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$OutdoorVariant` | `/heatSources/hybrid/outdoorVariant` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$ReminderDate` | `/heatSources/hybrid/reminderDate` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$ReminderEnable` | `/heatSources/hybrid/reminderEnable` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Hybrid$ReminderLapsed` | `/heatSources/hybrid/reminderLapsed` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Info` | `/heatSources/info` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$NumberOfStarts` | `/heatSources/hs1/numberOfStarts` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$PassiveCooling$InflowTemp` | `/heatSources/passiveCooling/inflowTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$PvContactState` | `/heatSources/pvContactState` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$ReturnTemperature` | `/heatSources/returnTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$StandbyMode` | `/heatSources/standbyMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$SystemPressure` | `/heatSources/systemPressure` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$SystemPressureRange` | `/heatSources/systemPressureRange` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$Type` | `/heatSources/hs1/type` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatSourcesResource$WorkingTime$TotalSystem` | `/heatSources/workingTime/totalSystem` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$ActiveSwitchProgram` | `/heatingCircuits/{hc}/activeSwitchProgram` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$ActualHumidity` | `/heatingCircuits/{hc}/actualHumidity` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$BoostDuration` | `/heatingCircuits/{hc}/boostDuration` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$BoostMode` | `/heatingCircuits/{hc}/boostMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$BoostRemainingTime` | `/heatingCircuits/{hc}/boostRemainingTime` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$BoostTemperature` | `/heatingCircuits/{hc}/boostTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$ChName` | `/heatingCircuits/{hc}/name` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$ControlType` | `/heatingCircuits/{hc}/controlType` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$Cooling$ControlType` | `/heatingCircuits/{hc}/cooling/controlType` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$Cooling$OperationMode` | `/heatingCircuits/{hc}/cooling/operationMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$Cooling$RoomTempSetpoint` | `/heatingCircuits/{hc}/cooling/roomTempSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$Cooling$SwitchPrograms$A` | `/heatingCircuits/{hc}/cooling/switchPrograms/A` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$Cooling$TemperatureLevels$On` | `/heatingCircuits/{hc}/cooling/temperatureLevels/on` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$CurrentRoomSetpoint` | `/heatingCircuits/{hc}/currentRoomSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$CurrentSuWiMode` | `/heatingCircuits/{hc}/currentSuWiMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$HeatCoolMode` | `/heatingCircuits/{hc}/heatCoolMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$HeatingType` | `/heatingCircuits/{hc}/heatingType` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$ManualRoomSetpoint` | `/heatingCircuits/{hc}/manualRoomSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$OperationMode` | `/heatingCircuits/{hc}/operationMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$OverallStatus` | `/heatingCircuits/{hc}/overallStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$RoomTemperature` | `/heatingCircuits/{hc}/roomtemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SetpointOptimization` | `/heatingCircuits/{hc}/setpointOptimization` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SuWiCoolingThreshold` | `/heatingCircuits/{hc}/suWiCoolingThreshold` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SuWiSwitchMode` | `/heatingCircuits/{hc}/suWiSwitchMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SuWiThreshold` | `/heatingCircuits/{hc}/suWiThreshold` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SwitchProgram$A` | `/heatingCircuits/{hc}/switchPrograms/A` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SwitchProgram$B` | `/heatingCircuits/{hc}/switchPrograms/B` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SwitchProgram$NameA` | `/heatingCircuits/{hc}/switchPrograms/nameA` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SwitchProgram$NameB` | `/heatingCircuits/{hc}/switchPrograms/nameB` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$SwitchProgramMode` | `/heatingCircuits/{hc}/switchProgramMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$TemperatureLevels$Comfort2` | `/heatingCircuits/{hc}/temperatureLevels/comfort2` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$TemperatureLevels$Eco` | `/heatingCircuits/{hc}/temperatureLevels/eco` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHeatingCircuitResource$TemporaryRoomSetpoint` | `/heatingCircuits/{hc}/temporaryRoomSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHolidayModeResource$DeleteHolidayMode` | `/holidayMode/` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyHolidayModeResource$HolidayActiveModes` | `/holidayMode/activeModes` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHolidayModeResource$HolidayConfiguration` | `/holidayMode/configuration` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHolidayModeResource$HolidayList` | `/holidayMode/list` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyHolidayModeResource$PostHolidayMode` | `/holidayMode` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyNotificationsResource$Notifications` | `/notifications` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyPoolResource$AdditionalHeater$PoolMode` | `/pool/additionalHeater/poolMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyPoolResource$CurrentTemp` | `/pool/currentTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyPoolResource$Enabled` | `/pool/enabled` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyPoolResource$SetpointTemp` | `/pool/setpointTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyRecordingsResource$EmonTotalBurner` | `/recordings/heatSources/emon/total/burner?interval=` | Optional history, not implemented |
| connectkeyprovider | `ConnectKeyRecordingsResource$EmonTotalElectricity` | `/recordings/heatSources/emon/total/electricity?interval=` | Optional history, not implemented |
| connectkeyprovider | `ConnectKeyRecordingsResource$EmonTotalOutputProduced` | `/recordings/heatSources/emon/total/outputProduced?interval=` | Optional history, not implemented |
| connectkeyprovider | `ConnectKeyRecordingsResource$EmonTotalOutputProducedHsX` | `/recordings/heatSources/hs/emon/total/outputProduced?interval=` | Optional history, not implemented |
| connectkeyprovider | `ConnectKeyRecordingsResource$EmonTotalSolar` | `/recordings/heatSources/emon/total/solar?interval=` | Optional history, not implemented |
| connectkeyprovider | `ConnectKeySolarCircuitsResource$CollectorTemperature` | `/solarCircuits/sc1/collectorTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySolarCircuitsResource$DhwTankBottomTemperature` | `/solarCircuits/sc1/dhwTankBottomTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySolarCircuitsResource$MaxCylinderTemperature` | `/solarCircuits/sc1/maxCylinderTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySolarCircuitsResource$MaxTemperatureReached` | `/solarCircuits/sc1/maxTemperatureReached` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySolarCircuitsResource$PumpModulation` | `/solarCircuits/sc1/pumpModulation` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySolarCircuitsResource$SolarYield` | `/solarCircuits/sc1/solarYield` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$AwayMode` | `/system/awayMode/enabled` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$Brand` | `/system/brand` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$Bus` | `/system/bus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$Country` | `/system/country` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$DateTime` | `/system/dateTime` | Excluded: private or administrative |
| connectkeyprovider | `ConnectKeySystemResource$EnergyTariff$Electricity` | `/system/energyTariff/electricity` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$EnergyTariff$Gas` | `/system/energyTariff/gas` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$EnergyTariff$Oil` | `/system/energyTariff/oil` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$EnergyTariff$Pv` | `/system/energyTariff/pv` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$GlobalSeasonOptimizer$CurrentMode` | `/system/globalSeasonOptimizer/currentMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$Info` | `/system/info` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$IsrcInstallationStatus` | `/system/iSRC/installationStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$IsrcSupportStatus` | `/system/iSRC/supportStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$LowNoise$Duration` | `/system/lowNoise/duration` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$LowNoise$Mode` | `/system/lowNoise/mode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$PowerGuard` | `/system/powerGuard/active` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$PowerLimitation` | `/system/powerLimitation/active` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SeasonOptimizer$CoolingThreshold` | `/system/seasonOptimizer/coolingThreshold` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SeasonOptimizer$HeatingThreshold` | `/system/seasonOptimizer/heatingThreshold` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SeasonOptimizer$Mode` | `/system/seasonOptimizer/mode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$Sensors$TemperaturesOutdoorT1` | `/system/sensors/temperatures/outdoor_t1` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SilentMode$Enabled` | `/system/silentMode/enabled` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SilentMode$PowerReduction` | `/system/silentMode/powerReduction` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SilentMode$StartTime` | `/system/silentMode/startTime` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$SilentMode$StopTime` | `/system/silentMode/stopTime` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$ChCurrentSetpoint` | `/system/variableTariff/ch/currentSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$ChHighPriceDelta` | `/system/variableTariff/ch/highPriceDelta` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$ChLowPriceDelta` | `/system/variableTariff/ch/lowPriceDelta` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$ChMidPriceSetpoint` | `/system/variableTariff/ch/midPriceSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$ChOptimization` | `/system/variableTariff/ch/optimization` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$ChStatus` | `/system/variableTariff/ch/status` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$CurrentPriceCategorization` | `/system/variableTariff/currentPriceCatagorization` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$DhwCurrentOpMode` | `/system/variableTariff/dhw/currentOpmode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$DhwHighPriceEnable` | `/system/variableTariff/dhw/highPriceEnable` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$DhwLowPriceEnable` | `/system/variableTariff/dhw/lowPriceEnable` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$DhwOptimization` | `/system/variableTariff/dhw/optimization` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$DhwStatus` | `/system/variableTariff/dhw/status` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$PriceInfo` | `/system/variableTariff/priceInfo` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$SupportStatus` | `/system/variableTariff/supportStatus` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeySystemResource$VariableTariff$TariffId` | `/system/variableTariff/tariffId` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$ExhaustFanLevel` | `/ventilation/zone1/exhaustFanLevel` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$FilterRemainingTime` | `/ventilation/zone1/filter/remainingTime` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$MaxIndoorAirQuality` | `/ventilation/zone1/maxIndoorAirQuality` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$MaxRelativeHumidity` | `/ventilation/zone1/maxRelativeHumidity` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$OperationMode` | `/ventilation/zone1/operationMode` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$SensorsSupplyTemp` | `/ventilation/zone1/sensors/supplyTemp` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyVentilationResource$SwitchProgram` | `/ventilation/zone1/switchPrograms/cp` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyVentilationResource$VentilationLevels` | `/ventilation/zone1/ventilationLevels` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyZonesResource$AverageActualHumidity` | `/zones/{zone}/averageActualHumidity` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyZonesResource$AverageCurrentTemperature` | `/zones/{zone}/averageCurrentTemperature` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyZonesResource$ChildLock` | `/zones/{zone}/childLock` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyZonesResource$Configuration` | `/zones/configuration` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$Cooling$ManualRoomSetpoint` | `/zones/{zone}/cooling/manualRoomSetpoint` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$Cooling$OperationMode` | `/zones/{zone}/cooling/operationMode` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$Cooling$TemporaryRoomSetpoint` | `/zones/{zone}/cooling/temporaryRoomSetpoint` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$CurrentRoomSetpoint` | `/zones/{zone}/currentRoomSetpoint` | Existing curated path; live schema still required |
| connectkeyprovider | `ConnectKeyZonesResource$Heating$ManualRoomSetpoint` | `/zones/{zone}/heating/manualRoomSetpoint` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$Heating$OperationMode` | `/zones/{zone}/heating/operationMode` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$Heating$TemporaryRoomSetpoint` | `/zones/{zone}/heating/temporaryRoomSetpoint` | Not released; semantics or adapter review pending |
| connectkeyprovider | `ConnectKeyZonesResource$SwitchPrograms$Cooling` | `/zones/{zone}/switchPrograms/cooling` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyZonesResource$SwitchPrograms$Heating` | `/zones/{zone}/switchPrograms/heating` | Structured format needs parser and device fixture |
| connectkeyprovider | `ConnectKeyZonesResource$ZonesList` | `/zones/list` | Not released; semantics or adapter review pending |
| connectkeyprovider | `DhwCircuits` | `/dhwCircuits` | Existing curated path; live schema still required |
| connectkeyprovider | `HeatingCircuits` | `/heatingCircuits` | Existing curated path; live schema still required |
| connectkeyprovider | `SolarCircuits` | `/solarCircuits` | Not released; semantics or adapter review pending |
| icomprovider | `IcomCircuitsResource$Dhw` | `/dhwCircuits` | Existing curated path; live schema still required |
| icomprovider | `IcomCircuitsResource$Heating` | `/heatingCircuits` | Existing curated path; live schema still required |
| icomprovider | `IcomCircuitsResource$Solar` | `/solarCircuits` | Not released; semantics or adapter review pending |
| icomprovider | `IcomCoolingCircuitsResource$RoomTempSetpoint` | `/heatingCircuits/{hc}/cooling/roomTempSetpoint` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$ActualTemperature` | `/dhwCircuits/{dhw}/actualTemp` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$ExtraDhwDuration` | `/dhwCircuits/{dhw}/chargeDuration` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$ExtraDhwSetpoint` | `/dhwCircuits/{dhw}/singleChargeSetpoint` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$ExtraDhwState` | `/dhwCircuits/{dhw}/charge` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$HolidayModeActivated` | `/dhwCircuits/{dhw}/holidayMode/activated` | Not released; semantics or adapter review pending |
| icomprovider | `IcomDhwCircuitsResource$OperationMode` | `/dhwCircuits/{dhw}/operationMode` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$SwitchProgram` | `/dhwCircuits/{dhw}/switchPrograms/A` | Structured format needs parser and device fixture |
| icomprovider | `IcomDhwCircuitsResource$TemperatureLevelHigh` | `/dhwCircuits/{dhw}/temperatureLevels/high` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$TemperatureLevelLow` | `/dhwCircuits/{dhw}/temperatureLevels/low` | Existing curated path; live schema still required |
| icomprovider | `IcomDhwCircuitsResource$TemperatureLevels` | `/dhwCircuits/{dhw}/temperatureLevels` | Existing curated path; live schema still required |
| icomprovider | `IcomGatewayResource$DateTime` | `/gateway/DateTime` | Excluded: private or administrative |
| icomprovider | `IcomGatewayResource$Uuid` | `/gateway/uuid` | Excluded: private or administrative |
| icomprovider | `IcomGatewayResource$VersionFirmware` | `/gateway/versionFirmware` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatSourcesResource$HsType` | `/heatSources/hs1/type` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatSourcesResource$Info` | `/heatSources/info` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$ActiveSwitchProgram` | `/heatingCircuits/{hc}/activeSwitchProgram` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$ControlType` | `/heatingCircuits/{hc}/controlType` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$CurrentRoomSetpoint` | `/heatingCircuits/{hc}/currentRoomSetpoint` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$CurrentSuWiMode` | `/heatingCircuits/{hc}/currentSuWiMode` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$HolidayModeActivated` | `/heatingCircuits/{hc}/holidayMode/activated` | Not released; semantics or adapter review pending |
| icomprovider | `IcomHeatingCircuitsResource$ManualRoomSetpoint` | `/heatingCircuits/{hc}/manualRoomSetpoint` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$OperationMode` | `/heatingCircuits/{hc}/operationMode` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$RoomTemperature` | `/heatingCircuits/{hc}/roomtemperature` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$SuWiSwitchMode` | `/heatingCircuits/{hc}/suWiSwitchMode` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$SwitchProgramA` | `/heatingCircuits/{hc}/switchPrograms/A` | Structured format needs parser and device fixture |
| icomprovider | `IcomHeatingCircuitsResource$SwitchProgramB` | `/heatingCircuits/{hc}/switchPrograms/B` | Structured format needs parser and device fixture |
| icomprovider | `IcomHeatingCircuitsResource$SwitchProgramMode` | `/heatingCircuits/{hc}/switchProgramMode` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$TemperatureLevels` | `/heatingCircuits/{hc}/temperatureLevels` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$TemperatureLevelsComfort` | `/heatingCircuits/{hc}/temperatureLevels/comfort2` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$TemperatureLevelsEco` | `/heatingCircuits/{hc}/temperatureLevels/eco` | Existing curated path; live schema still required |
| icomprovider | `IcomHeatingCircuitsResource$TemporaryRoomSetpoint` | `/heatingCircuits/{hc}/temporaryRoomSetpoint` | Existing curated path; live schema still required |
| icomprovider | `IcomHolidayModesResource$DhwMode` | `/system/holidayModes/hm/dhwMode` | Structured format needs parser and device fixture |
| icomprovider | `IcomHolidayModesResource$FixTemperature` | `/system/holidayModes/hm/fixTemperature` | Structured format needs parser and device fixture |
| icomprovider | `IcomHolidayModesResource$HcMode` | `/system/holidayModes/hm/hcMode` | Structured format needs parser and device fixture |
| icomprovider | `IcomHolidayModesResource$StartStop` | `/system/holidayModes/hm/startStop` | Structured format needs parser and device fixture |
| icomprovider | `IcomNotificationsResource$Notifications` | `/notifications` | Existing curated path; live schema still required |
| icomprovider | `IcomSystemResource$BusType` | `/system/bus` | Existing curated path; live schema still required |
| icomprovider | `IcomSystemResource$Country` | `/system/busReq?emsData=0804840401` | Excluded: private or administrative |
| icomprovider | `IcomSystemResource$Info` | `/system/info` | Existing curated path; live schema still required |
| icomprovider | `IcomVentilationResource$ExhaustFanLevel` | `/ventilation/zone1/exhaustFanLevel` | Existing curated path; live schema still required |
| icomprovider | `IcomVentilationResource$OperationMode` | `/ventilation/zone1/operationMode` | Existing curated path; live schema still required |
| rrcprovider | `ActualTemperature` | `/dhwCircuits/{dhw}/actualTemp` | Existing curated path; live schema still required |
| rrcprovider | `AwayMode` | `/system/awayMode/enabled` | Existing curated path; live schema still required |
| rrcprovider | `AwayTemperature` | `/system/awayMode/temperature` | Existing curated path; live schema still required |
| rrcprovider | `ClockProgram` | `/zones/zn/clockProgram` | Not released; semantics or adapter review pending |
| rrcprovider | `ControlKey` | `/heatingCircuits/hc/control` | Not released; semantics or adapter review pending |
| rrcprovider | `FirmwareVersion` | `/gateway/versionFirmware` | Existing curated path; live schema still required |
| rrcprovider | `HeatSourceType` | `/heatSources/type` | Existing curated path; live schema still required |
| rrcprovider | `HmipDeviceList` | `/devices/list` | Existing curated path; live schema still required |
| rrcprovider | `HmipDeviceName` | `/devices/dev/name` | Existing curated path; live schema still required |
| rrcprovider | `HmipDeviceZone` | `/devices/device/zone` | Not released; semantics or adapter review pending |
| rrcprovider | `HotWaterOperationMode` | `/dhwCircuits/{dhw}/operationMode` | Existing curated path; live schema still required |
| rrcprovider | `HotWaterSystem` | `/dhwCircuits/{dhw}/hotWaterSystem` | Not released; semantics or adapter review pending |
| rrcprovider | `HotWaterWeeklyPrograms` | `/programs/pg/week/dhwCircuits/dhw` | Unresolved path composition |
| rrcprovider | `Icon` | `/zones/zn/icon` | Not released; semantics or adapter review pending |
| rrcprovider | `Icons` | `/gateway/ui/icons` | Not released; semantics or adapter review pending |
| rrcprovider | `Info` | `/heatSources/info` | Existing curated path; live schema still required |
| rrcprovider | `Location` | `/system/location/coordinates` | Excluded: private or administrative |
| rrcprovider | `Name` | `/zones/zn/name` | Not released; semantics or adapter review pending |
| rrcprovider | `OpenWindowDetection` | `/zones/zn/openWindowDetection/enabled` | Not released; semantics or adapter review pending |
| rrcprovider | `RrcChClockProgramDayResource` | `/programs/pg/` | Unresolved path composition |
| rrcprovider | `RrcChClockProgramNameResource` | `/programs/pg/name` | Unresolved path composition |
| rrcprovider | `RrcChClockProgramResource` | `/programs/pg` | Unresolved path composition |
| rrcprovider | `RrcChClockProgramsResource` | `/programs/list` | Unresolved path composition |
| rrcprovider | `RrcChClockWeekProgramResource` | `/programs/pg/week` | Unresolved path composition |
| rrcprovider | `RrcChPrograms` | `/programs` | Unresolved path composition |
| rrcprovider | `Steps` | `/gateway/wizardStepsDone` | Not released; semantics or adapter review pending |
| rrcprovider | `Time` | `/gateway/time/current` | Not released; semantics or adapter review pending |
| rrcprovider | `TimeZone` | `/gateway/time/timeZone` | Not released; semantics or adapter review pending |
| rrcprovider | `UserMode` | `/zones/zn/userMode` | Not released; semantics or adapter review pending |
| rrcprovider | `Uuid` | `/gateway/uuid` | Excluded: private or administrative |
| rrcprovider | `Zone` | `/zones/zn` | Not released; semantics or adapter review pending |
| rrcprovider | `ZoneClockOverrideTemperature` | `/zones/zn/clockOverride/temperatureHeating` | Not released; semantics or adapter review pending |
| rrcprovider | `ZoneList` | `/zones/list` | Not released; semantics or adapter review pending |
| rrcprovider | `ZoneManualTemperature` | `/zones/zn/manualTemperatureHeating` | Not released; semantics or adapter review pending |
| rrcprovider | `ZoneTemperatureActual` | `/zones/zn/temperatureActual` | Not released; semantics or adapter review pending |
| rrcprovider | `ZoneTemperatureHeatingSetpoint` | `/zones/zn/temperatureHeatingSetpoint` | Not released; semantics or adapter review pending |
| rrcprovider | `Zones` | `/zones` | Not released; semantics or adapter review pending |
| watersoftenerprovider | `WaterSoftenerApplianceResource$ApplianceVersion` | `/system/appliance/versionFirmware` | Existing curated path; live schema still required |
| watersoftenerprovider | `WaterSoftenerApplianceResource$ModelType` | `/system/appliance/model` | Existing curated path; live schema still required |
| watersoftenerprovider | `WaterSoftenerConfiguringResource$FactoryReset` | `/gateway/factoryReset` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerConfiguringResource$UpdateTriggerRequest` | `/gateway/update/triggerRequest` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerGatewayResource$DateTime` | `/gateway/DateTime` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerGatewayResource$SerialId` | `/gateway/serialId` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerGatewayResource$TimeZone` | `/gateway/tzInfo/timeZone` | Existing curated path; live schema still required |
| watersoftenerprovider | `WaterSoftenerGatewayResource$Uuid` | `/gateway/uuid` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerGatewayResource$VersionFirmware` | `/gateway/versionFirmware` | Existing curated path; live schema still required |
| watersoftenerprovider | `WaterSoftenerGatewayResource$VersionHardware` | `/gateway/versionHardware` | Existing curated path; live schema still required |
| watersoftenerprovider | `WaterSoftenerGatewayResource$WifiMac` | `/gateway/wifi/mac` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerGatewayResource$WifiSsid` | `/gateway/wifi/ssid` | Excluded: private or administrative |
| watersoftenerprovider | `WaterSoftenerHolidayResource$HolidayMode` | `/swCircuits/sw1/holidayMode/enabled` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRecordingsResource$DailyRecordingsResource` | `/recordings/swCircuits/sw1/sensor/water?interval=31D` | Optional history, not implemented |
| watersoftenerprovider | `WaterSoftenerRecordingsResource$MonthlyRecordingsResource` | `/recordings/swCircuits/sw1/sensor/water?interval=24M` | Optional history, not implemented |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationEnabled` | `/swCircuits/sw1/regeneration/enabled` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationPhase` | `/swCircuits/sw1/regeneration/phase` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationSchedule` | `/swCircuits/sw1/regeneration/singleRegAppoint` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationTimeUntilNext` | `/swCircuits/sw1/regeneration/timeUntilNext` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationTotalProgressStatus` | `/swCircuits/sw1/regeneration/totalProgressStatus` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationTotalRemainingTime` | `/swCircuits/sw1/regeneration/totalRemainingTime` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerRegenerationResource$RegenerationsLog` | `/swCircuits/sw1/regeneration/log` | Optional history, not implemented |
| watersoftenerprovider | `WaterSoftenerSensorResource$AvailableWater` | `/swCircuits/sw1/sensor/availableWater` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerSensorResource$SaltLevel` | `/swCircuits/sw1/sensor/saltLevel` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerSensorResource$SaltLevelAlarm` | `/swCircuits/sw1/sensor/saltLevelAlarm` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerSensorResource$WaterFlow` | `/swCircuits/sw1/sensor/waterFlow` | Implemented read contract, device verification pending |
| watersoftenerprovider | `WaterSoftenerSystemResource$Brand` | `/system/brand` | Existing curated path; live schema still required |
| watersoftenerprovider | `WaterSoftenerSystemResource$Notifications` | `/notifications` | Existing curated path; live schema still required |
| wddw2provider | `ActualPower` | `/heatSources/hs1/actualPower` | Existing curated path; live schema still required |
| wddw2provider | `AirBoxTemperature` | `/dhwCircuits/dhw1/sensor/airBoxTemperature` | Existing curated path; live schema still required |
| wddw2provider | `ApplianceVersion` | `/system/appliance/versionFirmware` | Existing curated path; live schema still required |
| wddw2provider | `AtmosphericPressure` | `/dhwCircuits/dhw1/sensor/atmosphericPressure` | Existing curated path; live schema still required |
| wddw2provider | `Brand` | `/system/brand` | Existing curated path; live schema still required |
| wddw2provider | `BusType` | `/system/bus` | Existing curated path; live schema still required |
| wddw2provider | `Charge` | `/dhwCircuits/dhw1/charge` | Existing curated path; live schema still required |
| wddw2provider | `CurrentSetpoint` | `/dhwCircuits/dhw1/currentSetpoint` | Existing curated path; live schema still required |
| wddw2provider | `DateTime` | `/gateway/DateTime` | Excluded: private or administrative |
| wddw2provider | `ElectricityRecordings` | `/recordings/heatSources/hs1/sensor/electricity?interval=` | Optional history, not implemented |
| wddw2provider | `ElectricityTotalConsumption` | `/heatSources/electricityTotalConsumption` | Existing curated path; live schema still required |
| wddw2provider | `Enabled` | `/system/appliance/enabled` | Existing curated path; live schema still required |
| wddw2provider | `ExhaustFlueGasTemperature` | `/dhwCircuits/dhw1/sensor/exhaustFlueGasTemperature` | Existing curated path; live schema still required |
| wddw2provider | `ExternalTankTemperature` | `/dhwCircuits/dhw1/sensor/externalTankTemperature` | Existing curated path; live schema still required |
| wddw2provider | `FactoryReset` | `/gateway/factoryReset` | Excluded: private or administrative |
| wddw2provider | `FanSpeed` | `/dhwCircuits/dhw1/sensor/fanSpeed` | Existing curated path; live schema still required |
| wddw2provider | `GasFlow` | `/dhwCircuits/dhw1/sensor/gasFlow` | Existing curated path; live schema still required |
| wddw2provider | `GasRecordings` | `/recordings/heatSources/hs1/sensor/gas?interval=` | Optional history, not implemented |
| wddw2provider | `GasTotalConsumption` | `/heatSources/gasTotalConsumption` | Existing curated path; live schema still required |
| wddw2provider | `HardwareFirmware` | `/gateway/versionHardware` | Existing curated path; live schema still required |
| wddw2provider | `HeatExchangerFlueGasTemperature` | `/dhwCircuits/dhw1/sensor/heatExchangerFlueGasTemperature` | Existing curated path; live schema still required |
| wddw2provider | `HeatExchangerTemperature` | `/dhwCircuits/dhw1/sensor/heatExchangerTemperature` | Existing curated path; live schema still required |
| wddw2provider | `HolidayMode` | `/system/holidayMode` | Structured format needs parser and device fixture |
| wddw2provider | `InletTemperature` | `/dhwCircuits/dhw1/inletTemperature` | Existing curated path; live schema still required |
| wddw2provider | `LearningWeek` | `/dhwCircuits/dhw1/learningWeek` | Existing curated path; live schema still required |
| wddw2provider | `ManualSetpoint` | `/dhwCircuits/dhw1/manualsetpoint` | Existing curated path; live schema still required |
| wddw2provider | `ModelType` | `/system/appliance/model` | Existing curated path; live schema still required |
| wddw2provider | `MonitorValues` | `/dhwCircuits/dhw1/monitorValues` | Existing curated path; live schema still required |
| wddw2provider | `Notifications` | `/notifications` | Existing curated path; live schema still required |
| wddw2provider | `NumberOfShowersAvailable` | `/dhwCircuits/dhw1/numberOfShowersAvailable` | Existing curated path; live schema still required |
| wddw2provider | `NumberOfStarts` | `/heatSources/hs1/numberOfStarts` | Existing curated path; live schema still required |
| wddw2provider | `OperationHours` | `/heatSources/hs1/operationHours` | Existing curated path; live schema still required |
| wddw2provider | `OperationMode` | `/dhwCircuits/dhw1/operationMode` | Existing curated path; live schema still required |
| wddw2provider | `OperationSetpoints` | `/dhwCircuits/dhw1/operationSetpoints` | Existing curated path; live schema still required |
| wddw2provider | `OutletTemperature` | `/dhwCircuits/dhw1/outletTemperature` | Existing curated path; live schema still required |
| wddw2provider | `PowerPercentage` | `/heatSources/hs1/powerPercentage` | Existing curated path; live schema still required |
| wddw2provider | `Recirculation` | `/dhwCircuits/dhw1/recirculation/enabled` | Existing curated path; live schema still required |
| wddw2provider | `SafetyTemperature` | `/dhwCircuits/dhw1/safetyTemperature` | Existing curated path; live schema still required |
| wddw2provider | `SerialId` | `/gateway/serialId` | Excluded: private or administrative |
| wddw2provider | `SwitchProgram` | `/dhwCircuits/dhw1/switchPrograms/program1` | Structured format needs parser and device fixture |
| wddw2provider | `SystemUnits` | `/system/systemOfUnits` | Existing curated path; live schema still required |
| wddw2provider | `ThermalDisinfection` | `/dhwCircuits/dhw1/tdMode` | Existing curated path; live schema still required |
| wddw2provider | `TimeZone` | `/gateway/tzInfo/timeZone` | Existing curated path; live schema still required |
| wddw2provider | `UpdateTriggerRequest` | `/gateway/update/triggerRequest` | Excluded: private or administrative |
| wddw2provider | `Uuid` | `/gateway/uuid` | Excluded: private or administrative |
| wddw2provider | `VersionFirmware` | `/gateway/versionFirmware` | Existing curated path; live schema still required |
| wddw2provider | `WaterFlow` | `/dhwCircuits/dhw1/sensor/waterFlow` | Existing curated path; live schema still required |
| wddw2provider | `WaterRecordings` | `/recordings/dhwCircuits/dhw1/sensor/water?interval=` | Optional history, not implemented |
| wddw2provider | `WaterTotalConsumption` | `/dhwCircuits/waterTotalConsumption` | Existing curated path; live schema still required |
| wddw2provider | `WifiMac` | `/gateway/wifi/mac` | Excluded: private or administrative |
| wddw2provider | `WifiSsid` | `/gateway/wifi/ssid` | Excluded: private or administrative |
