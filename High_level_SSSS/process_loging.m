%% Script to pick out the desired IDs from the log file 
%% Doing a bit of cleaning 
clf
clear 
clc 
close all 
%% Loading in data 
% Specify the filename
filename = 'example.csv_05-01_08-56-38.csv';
%opts = detectImportOptions(filename,'PartialFieldRule','keep');

%gg= {'string', 'categorical', 'double'}
%opts = detectImportOptions(filename);

opts.VariableTypes = {'string', 'categorical', 'double'}; 

opts = detectImportOptions('01_08-56-38.csv');
opts.VariableTypes = {'string', 'string', 'double'}; % Assuming 'ID' and 'Time' are strings and 'Data' is double
dataTable = readtable('example.csv_05-01_08-56-38.csv', opts);


%opts.EmptyValue = {'NA', 'N/A', 'missing', 'NaN', 'Inf'}; % Specify values to treat as empty
%opts.PartialFieldRule={'keep'};
% Define the format of the 'Data' column as a string
%formatSpec = '%s';

% Read the CSV file into a table, specifying the format for the 'Data' column
%data = readtable(filename, 'Format', formatSpec);
%data = readtable(filename, 'ReadVariableNames', false);


% Read the CSV file into a table
%data = readtable(filename, 'Delimiter', ',');
data = readtable(filename,opts);

IDLabels=unique(data.ID); 


% Create empty matrices for each element in the cell array
for i = 1:numel(IDLabels)
    eval([IDLabels{i} ' = [];']);
    eval([IDLabels{i} 'Time = [];']);
    IDLabelsTime{i}=[IDLabels{i} 'Time'];
end

%%
for matrixNumber = 1:numel(IDLabels)
    % Get the current matrix variable name
    
    current_var_name = IDLabels{matrixNumber};
    current_var_name_Time = IDLabelsTime{matrixNumber};

    %Going though each of the entires in the sample data  
    for index=1:1:size(data,1) 
        if strcmp(data.ID{index},  current_var_name )
                eval([current_var_name_Time ' = [' current_var_name_Time ', data.Time(index)];']);
                temp=str2double(data.Data(index));
             %Hvordan fungere det lige???????? 
            if isnan(temp) == 0 && isempty(temp) == 0
                eval([current_var_name ' = [' current_var_name ', temp];'])
                else 
                % Extract numeric values using regular expression
                numeric_values = regexp(data.Data(index), '\d+\.\d+', 'match');
                if isempty(numeric_values{:})==1 
                    numeric_values = regexp(data.Data(index), '\d+\.\d?', 'match');
                end 
                if isempty(numeric_values{:}) ==0 
                    % Extract the nested cell array
                    nested_cell_array = numeric_values{1};
                    for i = 1:numel(nested_cell_array)
                        Temp(i,1) = str2double(nested_cell_array{i});
                    end
                    % Append to the end of the existing matrix
                    eval([current_var_name ' = [' current_var_name ', Temp];']);
                else 
                   eval([current_var_name ' = [' current_var_name ', vectorTemp];']);
                end 
            end   
        end
    end
end

% Initialize variables
min_value = Inf;  % Initialize to positive infinity
min_index = 0;     % Initialize to an invalid index

% Iterate through the cell array
for i = 1:numel(IDLabelsTime)
    % Get the name of the current matrix
    current_matrix_name = IDLabelsTime{i};
    
    % Get the value of the first entire of the current matrix
    current_value = eval([current_matrix_name '(1)']);
    
    % Compare the value with the current minimum
    if current_value < min_value
        min_value = current_value;  % Update minimum value
        min_index = i;               % Update index of the minimum value
    end
end

% Iterate through the cell array
for i = 1:numel(IDLabelsTime)
    % Get the name of the current matrix
    current_matrix_name = IDLabelsTime{i};
    
    eval([current_matrix_name ' = [' current_matrix_name '-min_value];'])
end












