%% 
clear 
clc 
clf 
close all 
%%

%% 
addpath('C:\Users\is123\Downloads\Distributed_system_3\Distributed_system_3')

%% Testing the logProcess function 
tic
 ADMM_1 = dataProc('ADMM1_05-09_12-54-40.csv') 
 ADMM_2 = dataProc('ADMM2_05-09_12-54-40.csv')
 ADMM_3 = dataProc('ADMM3_05-09_12-54-40.csv')
 pump2_ctrl = dataProc('pump_ctrl2_05-09_12-54-39.csv')
 pump3_ctrl = dataProc('pump_ctrl3_05-09_12-54-41.csv')
 pump1=dataProc('pump1_05-09_12-54-38.csv')
 pump2=dataProc('pump2_05-09_12-54-40.csv') 
 tow = dataProc('tower_05-09_12-54-36.csv')
 rw_con=dataProc('return_and_consumer_valve_ctrl_05-09_12-54-42.csv')
toc
%%
save('05-10_11-32-14.mat')
ADMM_1.x_i(:,125)
ADMM_2.x_i(:,125)
ADMM_3.x_i(:,125)
%% 
plot(tow.tank_tower_mm)
grid 





