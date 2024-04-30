%% Script to pick out the desired IDs from the log file 
%% Doing a bit of cleaning 
clf
clear 
clc 
close all 
%% Loading in data 
% Specify the filename
filename = 'example.csv_04-30_15-24-10.csv';

% Read the CSV file into a table
data = readtable(filename, 'Delimiter', ',');

IDLabels=unique(data.ID); 


% Create empty matrices for each element in the cell array
for i = 1:numel(IDLabels)
    eval([IDLabels{i} ' = [];']);
    eval([IDLabels{i} 'Time = [];']);
end

for matrixNumber = 1:numel(IDLabels)
   % Get the current matrix variable name
   current_var_name = IDLabels{matrixNumber};
    %Going though each of the entires in the sample data  
    for index=1:1:size(data,1) 
                 if strcmp(data.ID{index},  current_var_name )
                    vectorTemp = data.Data(index); 
                    % Extract numeric values using regular expression
                    numeric_values = regexp(vectorTemp, '\d+\.\d+', 'match');
                    if isempty(numeric_values{:})==1 
                         numeric_values = regexp(vectorTemp, '\d+\.\d?', 'match');
                    end 
                    if isempty(numeric_values{:}) ==0 
                        % Extract the nested cell array
                        nested_cell_array = numeric_values{1};
                        for i = 1:numel(nested_cell_array)
                            Temp(i,1) = str2double(nested_cell_array{i});
                        end
                        % Append to the end of the existing matrix
                        eval([current_var_name ' = [' current_var_name ', Temp];']);
                    end 
                    eval([current_var_name ' = [' current_var_name ', vectorTemp];'])

                end

    end 
end

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
        if isempty(numeric_values{:})==1 
             numeric_values = regexp(vectorTemp, '\d+\.\d?', 'match');
        end 
        % Extract the nested cell array
        nested_cell_array = numeric_values{1};
        for i = 1:numel(nested_cell_array)
            Temp(i,1) = str2double(nested_cell_array{i});
        end
        secret_data = [secret_data,Temp];
    end
end





