%% 
clear 
clc 
clf 
close all 

%% Loading the files
addpath("C:\Users\Fie\OneDrive - Aalborg Universitet\UNI2\10.THE FINAL ONE\Matlab\Logged_data\ll_control_test")
pump1 = logProcces('pump_ctrl2_05-06_10-56-25.csv')
pump2 = logProcces('pump_ctrl3_05-06_10-56-27.csv')
consumption_valve1 =logProcces('consumption_valve1_05-06_10-56-28.csv')
consumption_valve2 =logProcces('consumption_valve2_05-06_10-56-28.csv')


save('05-06_10-56.mat')
%%
clear 
%folder = "Logging/Log_files/"
load('05-02_11-32.mat') 
%% Lil things i need

%Farver
    Blue = "#0072BD";
    Orange = "#D95319";
    Yellow =  "#EDB120";
    Purple = "#7E2F8E";
    Green = "#77AC30";
    Lightblue = "#4DBEEE";
    Red = "#A2142F";

%Farve på plots fordi jeg er for doven til at ændre det flere steder
    p1_flow = Orange;
    p1_ref  = Blue;
    p2_flow = Yellow;
    p2_ref  = Purple;

    v1_flow = Orange;
    v1_ref  = Blue;
    v2_flow = Yellow;
    v2_ref  = Purple;




%% Pump station 1 figure

f=figure()
start = 100;
plot_end = 1400;

subplot(2,1,1)
stairs(pump1.refTime-start, pump1.ref, color=p1_ref)
hold on
plot(pump1.flowTime-start, pump1.flow, color =p1_flow)
grid
legend('Reference', 'Measurement', Location='northwest')
title("")
xlabel("Time [s]")
xlim([0 plot_end])
xticks(0:200:plot_end)
ylim([0.05 0.35])
ylabel("Flow [m^3/h]")
subplot(2,1,2)
plot(pump1.Pump_percentageTime-start, pump1.Pump_percentage, color =p1_flow)
xlim([0 plot_end])
xticks(0:200:plot_end)
xlabel("Time [s]")
ylabel("Pump frequency [0-100]")
legend("Actuation", Location='northwest')
grid
title("")
fontname(f,'Times')
%exportgraphics(f,'PS1_PI_Performance.pdf')
%% Pump station 2 figure

f=figure()

start = 100;
plot_end = 1400;

subplot(2,1,1)
stairs(pump2.refTime-start, pump2.ref, color=p2_ref)
hold on
plot(pump2.flowTime-start, pump2.flow, color =p2_flow)
grid
legend('Reference', 'Measurement', Location='northwest')
title("")
xlabel("Time [s]")
xlim([0 plot_end])
xticks(0:200:plot_end)
ylim([0.05 0.35])
ylabel("Flow [m^3/h]")
subplot(2,1,2)
plot(pump2.Pump_percentageTime-start, pump2.Pump_percentage, color =p2_flow)
xlabel("Time [s]")
xlim([0 plot_end])
xticks(0:200:plot_end)
ylim([56 64])
ylabel("Pump frequency [0-100]")
legend("Actuation", Location='northwest')
grid
title("")
fontname(f,'Times')
%exportgraphics(f,'PS2_PI_Performance.pdf')
%% Krydskobling plot af pumperne
f=figure()

start = 555;
plot_end = 250;

subplot(2,1,1)
stairs(pump1.refTime-start, pump1.ref, color=p1_ref)
hold on
stairs(pump2.refTime-start, pump2.ref, color = p2_ref)
plot(pump1.flowTime-start, pump1.flow, color =p1_flow)
plot(pump2.flowTime-start, pump2.flow, color= p2_flow)
hold off
grid
legend('Reference pump 1', 'Reference pump 2', 'Measurement pump 1', 'Measurement pump 2', Location='northwest')
title("")
xlabel("Time [s]")
xlim([0 plot_end])
ylim([0.18 0.35])
ylabel("Flow [m^3/h]")
subplot(2,1,2)
plot(pump1.Pump_percentageTime-start, pump1.Pump_percentage, color =p1_flow)
hold on
plot(pump2.Pump_percentageTime-start, pump2.Pump_percentage, color= p2_flow)
xlabel("Time [s]")
xlim([0 plot_end])
ylim([60 73])
ylabel("Pump frequency [0-100]")
legend("Pump 1", "Pump 2", Location='northwest')
grid
title("")
fontname(f,'Times')
%exportgraphics(f,'PS_PI_cross.pdf')
%% %% Plot af begge pumper
f=figure()

start = 500;
plot_end = 1000;

subplot(2,1,1)
stairs(pump1.refTime-start, pump1.ref, color=p1_ref)
hold on
stairs(pump2.refTime-start, pump2.ref, color = p2_ref)
plot(pump1.flowTime-start, pump1.flow, color =p1_flow)
plot(pump2.flowTime-start, pump2.flow, color= p2_flow)
hold off
grid
legend('Reference pump 1', 'Reference pump 2', 'Measurement pump 1', 'Measurement pump 2', Location='southwest')
title("")
xlabel("Time [s]")
xlim([0 plot_end])
xticks(0:200:plot_end)
ylim([0 0.3])
ylabel("Flow [m^3/h]")
subplot(2,1,2)
plot(pump1.Pump_percentageTime-start, pump1.Pump_percentage, color =p1_flow)
hold on
plot(pump2.Pump_percentageTime-start, pump2.Pump_percentage, color= p2_flow)
xlabel("Time [s]")
xlim([0 plot_end])
xticks(0:200:plot_end)
ylim([50 70])
ylabel("Pump frequency [0-100]")
legend("Pump 1", "Pump 2", Location="southwest")
grid
title("")
fontname(f,'Times')
%exportgraphics(f,'PS_PI_Both.pdf')
%% Consumption valve 1 only

f=figure()

start = 2000;
plot_end = 2000;

subplot(2,1,1)
stairs(consumption_valve1.referenceTime-start, consumption_valve1.reference, color=v1_ref)
hold on
plot(consumption_valve1.flowTime-start, consumption_valve1.flow, color =v1_flow)
grid
legend('Reference', 'Measurement')
title("")
xlabel("Time [s]")
xlim([0 plot_end])
ylim([0.13 0.26])
ylabel("Flow [m^3/h]")
subplot(2,1,2)
plot(consumption_valve1.opening_degreeTime-start, consumption_valve1.opening_degree, color =v1_flow)
xlabel("Time [s]")
xlim([0 plot_end])
ylim([55 83])
ylabel("Opening degree [0-100]")
legend("Valve 1")
grid
title("")
fontname(f,'Times')
%exportgraphics(f,'Consumption_valve_1.pdf')
%% Consumption, both valves

f=figure()

start = 200;
plot_end = 1600;

subplot(2,1,1)
stairs(consumption_valve1.referenceTime-start, consumption_valve1.reference, color=v1_ref)
hold on
stairs(consumption_valve2.referenceTime-start, consumption_valve2.reference, color = v2_ref)
plot(consumption_valve1.flowTime-start, consumption_valve1.flow, color =v1_flow)
plot(consumption_valve2.flowTime-start, consumption_valve2.flow, color= v2_flow)
hold off
grid
legend('Reference valve 1', 'Reference valve 2', 'Measurement valve 1', 'Measurement valve 2', Location='northwest')
title("")
xlabel("Time [s]")
xlim([0 plot_end])
ylim([0 0.36])
ylabel("Flow [m^3/h]")
subplot(2,1,2)
plot(consumption_valve1.opening_degreeTime-start, consumption_valve1.opening_degree, color =v1_flow)
hold on
plot(consumption_valve2.opening_degreeTime-start, consumption_valve2.opening_degree, color= v2_flow)
xlabel("Time [s]")
xlim([0 plot_end])
ylabel("Opening degree [0-100]")
legend("Valve 1", "Valve 2", Location='northwest')
grid
title("")
fontname(f,'Times')
%exportgraphics(f,'Consumption_valve_both.pdf')






