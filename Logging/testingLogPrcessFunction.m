%% 
clear 
clc 
clf 
close all 

%% Testing the logProcess function 
rw_con=logProcces('return_and_consumer_valve_ctrl_05-01_13-51-14.csv');
ADMM_1 = logProcces('ADMM1_05-01_13-51-15.csv')
ADMM_2 = logProcces('ADMM2_05-01_13-51-15.csv')
ADMM_3 = logProcces('ADMM3_05-01_13-51-15.csv')
pump2_ctrl = logProcces('pump_ctrl2_05-01_13-51-12.csv')
pump3_ctrl = logProcces('pump_ctrl3_05-01_13-51-16.csv')
tow = logProcces('tower_05-01_13-51-15.csv')

save('05-01_13-51-15.mat')

%%
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve1Time/60, rw_con.Flow_valve1 + rw_con.Flow_valve2)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured")
