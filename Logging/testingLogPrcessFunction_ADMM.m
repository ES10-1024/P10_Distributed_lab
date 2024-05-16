%% 
clear 
clc 
clf 
close all 
%%

%% 
addpath('C:\Users\is123\Downloads\OneDrive_1_6.5.2024')
addpath('C:\Users\is123\Downloads\New simData\global')
addpath('C:\Users\is123\Downloads\New simData\consensus ADMM')

%% Testing the logProcess function 
tic
%rw_con=logProcces('return_and_consumer_valve_ctrl_05-16_11-04-43.csv');
ADMM_1 = dataProc('ADMM1_05-16_15-07-57.csv')
ADMM_2 = dataProc('ADMM2_05-16_15-07-57.csv')
ADMM_3 = dataProc('ADMM3_05-16_15-07-57.csv')
%pump2_ctrl = logProcces('pump_ctrl2_05-16_11-04-39.csv')
%pump3_ctrl = logProcces('pump_ctrl3_05-16_11-04-41.csv')
pump1 = dataProc('pump1_05-16_15-07-55.csv')
pump2 = dataProc('pump2_05-16_15-07-57.csv')
%%%globalCon = dataProc('global_control_05-16_13-23-06.csv')

tow = dataProc('tower_05-16_15-07-53.csv')
toc
%%
save('short_new_sim_data_ADMM.mat')
ADMM_1.x_i(:,125)
ADMM_2.x_i(:,125)
ADMM_3.x_i(:,125)
%% 
plot(tow.tank_tower_mm)
grid 





