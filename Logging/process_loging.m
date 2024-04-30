%% Script to pick out the desired IDs from the log file 
%% Doing a bit of cleaning 
clf
clear 
clc 
close all 
%% Loading in data 
% Specify the filename
filename = 'main_tower_04-30_13-31-00.csv';

% Read the CSV file into a table
data = readtable(filename, 'Delimiter', ',');

%% picking out the desired IDs
% Initialize variables to store the data which is desired to pick 
b1_data = [];
secret_data = [];

% Loop through the rows of the table
for index = 1:size(data, 1)
    %Can be used if only a scalar is desired (maybe else try using str2double, around the data which is picked out)  
    % Extract 'b1' data (b1 is the ID given, it can be anything given) 
    if strcmp(data.ID{index}, 'b1')
        b1_data = [b1_data; data.Data(index)];
    end
    %Should work for a vector 
    % Extract 'secret' data (secret is the ID given, it can be anything given)
    if strcmp(data.ID{index}, 'secret')
        vectorTemp = data.Data(index); 
        % Extract numeric values using regular expression
        numeric_values = regexp(vectorTemp, '\d+\.\d+', 'match');
        % Extract the nested cell array
        nested_cell_array = numeric_values{1};
        for i = 1:numel(nested_cell_array)
            Temp(i,1) = str2double(nested_cell_array{i});
        end
        secret_data = [secret_data,Temp];
    end
end

