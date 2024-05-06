%% 
clear 
clc 
clf 
close all 
%%

%% 
addpath('C:\Users\is123\Downloads\OneDrive_1_6.5.2024')

%% Testing the logProcess function 
tic
rw_con=dataProc('return_and_consumer_valve_ctrl_05-02_11-32-16.csv');
 ADMM_1 = dataProc('ADMM1_05-02_11-32-14.csv') 
 ADMM_2 = dataProc('ADMM2_05-02_11-32-14.csv')
 ADMM_3 = dataProc('ADMM3_05-02_11-32-14.csv')
 pump2_ctrl = dataProc('pump_ctrl2_05-02_11-32-13.csv')
 pump3_ctrl = dataProc('pump_ctrl3_05-02_11-32-14.csv')
 pump1=dataProc('pump1_05-02_11-32-12.csv')
 pump2=dataProc('pump2_05-02_11-32-14.csv') 
 tow = dataProc('tower_05-02_11-32-10.csv')
toc
%%
save('05-02_11-32-14.mat')
ADMM_1.x_i(:,125)
ADMM_2.x_i(:,125)
ADMM_3.x_i(:,125)
%% 
plot(tow.tank_tower_mm)
grid 





