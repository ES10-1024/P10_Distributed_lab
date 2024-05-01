%% 
clear 
clc 
clf 
close all 

%% Testing the logProcess function 
filename='return_and_consumer_valve_ctrl_05-01_12-53-00.csv'; 

log=logProcces(filename); 
%% 
plot(log.Flow_valve1Time,log.Flow_valve1)