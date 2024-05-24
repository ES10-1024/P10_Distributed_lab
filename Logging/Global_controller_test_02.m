%% 
clear 
clc 
clf 
close all 

%% Testing the logProcess function 
tic

folder = "C:\Users\pppc\Desktop\Test_data_Lau_lauridsen\Global_controller_2\"
pump2_ctrl = dataProc(folder+'pump_ctrl1_05-23_08-28-41.csv')
pump3_ctrl = dataProc(folder+'pump_ctrl2_05-23_08-28-41.csv')
rw_con= dataProc(folder+'return_and_consumer_valve_ctrl_05-23_08-28-40.csv');
global_con = dataProc(folder+'global_control_05-23_08-28-40.csv')
toc

save(folder+'05-23_06-28.mat')
%%
clear 
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Global_controller_1\"
%folder = "C:\Users\pppc\Desktop\Test_data_Lau_lauridsen"
load(folder+'05-07_11-24.mat')
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Global_controller_1\"
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
pump1 = global_con;

f = figure('Position',[10 10 900 600])
offset=pump1.SolutionTime(1)

sum_flow_time = pump3_ctrl.flowTime(1)-offset:1:pump3_ctrl.flowTime(end)-offset;
sum_flow = interp1(pump2_ctrl.flowTime-offset,pump2_ctrl.flow,sum_flow_time) + interp1(pump3_ctrl.flowTime-offset,pump3_ctrl.flow,sum_flow_time);
sum_flow_command = interp1(pump2_ctrl.refTime-offset,pump2_ctrl.ref, sum_flow_time,'previous') + interp1(pump3_ctrl.refTime-offset,pump3_ctrl.ref,sum_flow_time,'previous');

consumption_time = rw_con.Flow_valve1Time(1)-offset:1:rw_con.Flow_valve1Time(end)-offset
sum_consumption = interp1(rw_con.Flow_valve1Time-offset,rw_con.Flow_valve1, consumption_time) + interp1(rw_con.Flow_valve2Time-offset,rw_con.Flow_valve2, consumption_time);



i=0;
offset=pump1.SolutionTime(1)
for l = pump1.SolutionTime(1:124)
    clf
    i=i+1;
    disp(i)
    
    %Electricity price 
    tiledlayout(4,1, "TileSpacing","compact")
    %Prediction
    nexttile
    pump1.electricity_price(:,i)
    price_prediction_time = pump1.Simulated_hourTime(i)-offset + (0:23)*600;
    stairs(price_prediction_time/600, pump1.electricity_price(:,i),'color',"#EDB120")
    hold on
    %past
    stairs((pump1.Simulated_hourTime(1:i)-offset)/600,pump1.electricity_price(1,1:i),'Color',	"#77AC30")
    ylabel('Electricity price [EUR/kWh]')
    xlabel('Time [h_a]')
    grid 
    xlim([(pump1.SolutionTime(1)-offset)/600 (pump1.SolutionTime(1)-offset)/600+100])
    ylim([0 0.2])

    
   
    %Flow
    nexttile
    %Predicted flow
    sum_flow_prediction1 = pump1.Solution(1:2:end,i) + pump1.Solution(2:2:end,i);       %Flow prediction, both pumps based on solution from pump1
    sum_flow_prediction1_time = pump1.Simulated_hourTime(i)-offset + (0:23)*600;
    
    stairs(sum_flow_prediction1_time/600,sum_flow_prediction1, 'Color',"#EDB120")
    hold on
    %Past flow
    [~,idx1] = min(abs(sum_flow_time-l+offset));
    plot(sum_flow_time(1:idx1)/600, movmean(sum_flow(1:idx1),60), 'Color',	"#7E2F8E")
    %Past commands
    [~,idx2] = min(abs(sum_flow_time-l+offset));
    plot(sum_flow_time(1:idx2)/600, sum_flow_command(1:idx2), 'color', "#77AC30")
    ylabel('Sum of flows [m^3/h]')
    xlabel('Time [h_a]')
    ylim([0 0.6])
    xlim([(pump1.SolutionTime(1)-offset)/600 (pump1.SolutionTime(1)-offset)/600+100])
    grid
    

    %Volume in tower
    nexttile
    %Prediction
    inflow_volume = cumsum(sum_flow_prediction1)*1/6*1000;    %1/6 is time acceleration *1000 is m^3 to L
    outflow_volume1 = cumsum(pump1.demand_pred(:,i))*1/6*1000;
    tower_volume1 = pump1.tower_tank_level(i)*0.283 + inflow_volume - outflow_volume1;
    tower_volume1 = [pump1.tower_tank_level(i)*0.283; tower_volume1];
    sum_flow_prediction1_time = pump1.Simulated_hourTime(i)-offset + (0:24)*600;

    plot(sum_flow_prediction1_time/600,tower_volume1, 'color', 	"#EDB120")
    hold on
    %Past
    [~,idx] = min(abs(rw_con.tank_tower_mmTime-l));
    plot((rw_con.tank_tower_mmTime(1:idx)-offset)/600,rw_con.tank_tower_mm(1:idx)*0.283, 'Color',	"#7E2F8E")
    yline(28)
    yline(155)
    ylabel("Volume in tower [L]")
    xlabel('Time [h_a]')
    ylim([20 170])
    xlim([(pump1.SolutionTime(1)-offset)/600 (pump1.SolutionTime(1)-offset)/600+100])
    grid 

    %Demand
    nexttile
    %Prediction
    stairs(price_prediction_time/600, pump1.demand_pred(:,i), 'Color',"#EDB120")
    hold on
    %stairs(price_prediction_time/600, pump1.demand_pred(:,i))
    %stairs(price_prediction_time/600, pump1.demand_pred(:,i))
    %Flow
    [~,idx3] = min(abs(consumption_time-l+offset));
    plot(consumption_time(1:idx3)/600, movmean(sum_consumption(1:idx3),60), 'Color',	"#7E2F8E")
    %Commanded
    [~,idx] = min(abs(rw_con.DemandTime-l))
    plot(rw_con.DemandTime(1:idx)/600-offset/600,rw_con.Demand(1:idx),'Color',	"#77AC30")
    ylim([0 0.4])
    xlim([(pump1.SolutionTime(1)-offset)/600 (pump1.SolutionTime(1)-offset)/600+100])
    grid
    lgd = legend("Prediction", "Measured", "Commanded", 'Orientation','Horizontal')
    lgd.Layout.Tile = 'south';
    ylabel('Consumption [m^3/h]')
    xlabel('Time [h_a]')
    

    fontname(f,"Times")
    exportgraphics(f,folder+"plot.gif", Append=true)
    if(i==80)
        exportgraphics(f,folder+"Global_control_prediction.pdf", Append=true) 
    end

    if(i==80)
    Global.tower_vol = rw_con.tank_tower_mm(1:idx3)*0.283;
    Global.tower_vol_time = (rw_con.tank_tower_mmTime(1:idx3)-offset);

    Global.tower_vol_prediction = tower_volume1
    Global.tower_vol_prediction_time = sum_flow_prediction1_time/600;

    Global.flow_time = sum_flow_time(1:idx1)/600;
    Global.flow = sum_flow_command(1:idx1);

    Global.flow_prediction = sum_flow_prediction1
    Global.flow_prediction_time = sum_flow_prediction1_time/600

    
    save(folder+'Global_compaison.mat', 'Global')
    end
end


