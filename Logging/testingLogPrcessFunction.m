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

%save('05-01_13-51-15.mat')

%% Evaluate valve controller
clf
subplot(1,3,1)
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve1Time/60, rw_con.Flow_valve1 + rw_con.Flow_valve2)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured sum")

subplot(1,3,2)
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve1Time/60, rw_con.Flow_valve1)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured valve 1")

subplot(1,3,3)
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve2Time/60, rw_con.Flow_valve2)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured valve 2")

%% Eavluate pump flow controller
clf
subplot(1,2,1)
stairs(pump2_ctrl.refTime, pump2_ctrl.ref)
hold on
plot(pump2_ctrl.flowTime, movmean(pump2_ctrl.flow,10))
ylim([0.025 0.2])

subplot(1,2,2)
stairs(pump3_ctrl.refTime, pump3_ctrl.ref)
hold on
plot(pump3_ctrl.flowTime, movmean(pump3_ctrl.flow,10))
ylim([0.025 0.2])

%% Evaluate high level controller

%Figuring out if the solution is the correct one is a job for Simon
%I will make a gif ;)

