%% 
clear 
clc 
clf 
close all 

%% Testing the logProcess function 
rw_con=logProcces('return_and_consumer_valve_ctrl_05-02_11-32-16.csv');
ADMM_1 = logProcces('ADMM1_05-02_11-32-14.csv')
ADMM_2 = logProcces('ADMM2_05-02_11-32-14.csv')
ADMM_3 = logProcces('ADMM3_05-02_11-32-14.csv')
pump2_ctrl = logProcces('pump_ctrl2_05-02_11-32-13.csv')
pump3_ctrl = logProcces('pump_ctrl3_05-02_11-32-14.csv')
pump1=logProcces('pump1_05-02_11-32-12.csv')
pump2=logProcces('pump2_05-02_11-32-14.csv')

tow = logProcces('tower_05-02_11-32-10.csv')
%%
save('05-02_11-32-14.mat')
ADMM_1.x_i(:,125)
ADMM_2.x_i(:,125)
ADMM_3.x_i(:,125)
%% 
plot(tow.tank_tower_mm)
grid 





