%% 
clear 
clc 
clf 
close all 

%% Testing the logProcess function 
tic

folder = "C:\Users\pppc\Desktop\Test_data_Lau_lauridsen\Global_controller\"
pump2_ctrl = dataProc(folder+'pump_ctrl1_05-07_11-24-00.csv')
pump3_ctrl = dataProc(folder+'pump_ctrl2_05-07_11-24-00.csv')
rw_con= dataProc(folder+'return_and_consumer_valve_ctrl_05-07_11-24-12.csv');
global_con = dataProc(folder+'global_control_05-07_11-24-00.csv')
toc

save(folder+'05-07_11-24.mat')
%%
clear 
folder = "Logging/Log_files/"
folder = "C:\Users\pppc\Desktop\Test_data_Lau_lauridsen"
load(folder+'05-03_13-34.mat')

%% Evaluate valve controller
clf
subplot(1,3,1)
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve1Time/60, rw_con.Flow_valve1 + rw_con.Flow_valve2)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured sum")
ylim([0 0.7])

subplot(1,3,2)
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve1Time/60, rw_con.Flow_valve1)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured valve 1")
ylim([0 0.7])

subplot(1,3,3)
plot(rw_con.DemandTime/60, rw_con.Demand, rw_con.Flow_valve2Time/60, rw_con.Flow_valve2)
xlabel("Time  [min]")
ylabel("Flow [m^3/h]")
legend("Demanded","Measured valve 2")
ylim([0 0.7])

%% Eavluate pump flow controller
clf
subplot(1,2,1)
yyaxis left
plot(pump2_ctrl.flowTime, movmean(pump2_ctrl.flow,20))
hold on
stairs(pump2_ctrl.refTime, pump2_ctrl.ref)
ylim([0.025 0.3])
ylabel("Flow [m^3/h]")
yyaxis right
plot(pump2_ctrl.Pump_percentageTime(100:end), pump2_ctrl.Pump_percentage(100:end))
ylabel("Actuation [0-100]")

subplot(1,2,2)
yyaxis left
plot(pump3_ctrl.flowTime, movmean(pump3_ctrl.flow,20))
hold on
stairs(pump3_ctrl.refTime, pump3_ctrl.ref)
ylim([0.025 0.3])
ylabel("Flow [m^3/h]")
yyaxis right
plot(pump3_ctrl.Pump_percentageTime(100:end), pump3_ctrl.Pump_percentage(100:end))
ylabel("Actuation [0-100]")





%% Evaluate high level controller



%Figuring out if the solution is the correct one is a job for Simon
%I will make a gif ;)
f = figure('Position',[10 10 900 600])

sum_flow_time = 1:pump3_ctrl.flowTime(end);
sum_flow = interp1(pump2_ctrl.flowTime,pump2_ctrl.flow,sum_flow_time) + interp1(pump3_ctrl.flowTime,pump3_ctrl.flow,sum_flow_time);
sum_flow_command = interp1(pump2_ctrl.refTime,pump2_ctrl.ref, sum_flow_time,'previous') + interp1(pump3_ctrl.refTime,pump3_ctrl.ref,sum_flow_time,'previous');

consumption_time = 1:rw_con.Flow_valve1Time(end)
sum_consumption = interp1(rw_con.Flow_valve1Time,rw_con.Flow_valve1, consumption_time) + interp1(rw_con.Flow_valve2Time,rw_con.Flow_valve2, consumption_time);



i=0;
for l = pump1.SolutionTime
    clf
    i=i+1;
    disp(i)
    
    %Electricity price 
    subplot(2,2,1)
    %Prediction
    pump1.electricity_price(:,i)
    price_prediction_time = pump1.Simulated_hour(i)*600 + (-1:22)*600;
    stairs(price_prediction_time/600, pump1.electricity_price(:,i))
    hold on
    stairs(pump1.Simulated_hour(1:i)-1,pump1.electricity_price(1:i,1))
    ylabel('Electricty price [EUR/kWh]')
    xlabel('Time [h_s]')
    grid 
    xlim([0 pump1.SolutionTime(end)/600])
    ylim([min(min(squeeze(pump1.electricity_price))) max(max(squeeze(pump1.electricity_price)))])

    
   
    %Flow
    subplot(2,2,2)
    %Predicted flow
    sum_flow_prediction1 = pump1.Solution(1:2:end,i) + pump1.Solution(2:2:end,i);       %Flow prediction, both pumps based on solution from pump1
    sum_flow_prediction1_time = pump1.Simulated_hour(i)*600 + (-1:22)*600;
    stairs(sum_flow_prediction1_time/600,sum_flow_prediction1)
    hold on
    %Past flow
    [~,idx] = min(abs(sum_flow_time-l));
    plot(sum_flow_time(1:idx)/600, movmean(sum_flow(1:idx),60))
    %Past commands
    [~,idx] = min(abs(sum_flow_time-l));
    plot(sum_flow_time(1:idx)/600, sum_flow_command(1:idx))
    ylabel('Sum of flow [m^3/h_s]')
    xlabel('Time [h_s]')
    ylim([0 0.6])
    xlim([0 pump1.SolutionTime(end)/600])
    

    %Volume in tower
    subplot(2,2,3)
    %Prediction
    inflow_volume = cumsum(sum_flow_prediction1)*1/6*1000;    %1/6 is time acceleration *1000 is m^3 to L
    outflow_volume = cumsum(pump1.demand_pred(:,i))*1/6*1000;
    tower_volume = pump1.tower_tank_level(i)*0.283 + inflow_volume - outflow_volume;
    tower_volume = [pump1.tower_tank_level(i)*0.283; tower_volume];
    sum_flow_prediction1_time = pump1.Simulated_hour(i)*600 + (-1:23)*600;
    plot(sum_flow_prediction1_time/600,tower_volume)
    hold on
    %Past
    [~,idx] = min(abs(rw_con.tank_tower_mmTime-l));
    plot(rw_con.tank_tower_mmTime(1:idx)/600,rw_con.tank_tower_mm(1:idx)*0.283)
    yline(28)
    yline(155)
    ylabel("Volume in tower [L]")
    xlabel('Time [h_s]')
    ylim([20 170])
    xlim([0 pump1.SolutionTime(end)/600])

    %Demand
    subplot(2,2,4)
    %Prediction
    stairs(price_prediction_time/600, pump1.demand_pred(:,i))
    hold on
    %Flow
    [~,idx] = min(abs(consumption_time-l));
    plot(consumption_time(1:idx)/600, movmean(sum_consumption(1:idx),1))
    %Commanded
    [~,idx] = min(abs(rw_con.DemandTime-l));
    plot(rw_con.DemandTime(1:idx)/600,rw_con.Demand(1:idx))
    ylim([0 0.6])
    xlim([0 pump1.SolutionTime(end)/600])
    


    drawnow
    pause(0.3)
end


