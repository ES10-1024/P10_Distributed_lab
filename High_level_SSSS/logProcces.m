function [log] = logProcces(filename)
%% Function to pick out the desired IDs from the log file 
%Input filename, the file it is desired to work with, including .csv! 
%Output log, returns a struct with the data and sampling time

%% Loading in data 
opts = detectImportOptions(filename);
opts.VariableTypes = {'string', 'string', 'double'}; 

data = readtable(filename, opts);


%% Creating empty matrices for each ID 

IDLabels=unique(data.ID); 
for i = 1:numel(IDLabels)
    eval([IDLabels{i} ' = [];']);
    eval([IDLabels{i} 'Time = [];']);
    IDLabelsTime{i}=[IDLabels{i} 'Time'];
end

%% Picking out the data for each of the IDs
for matrixNumber = 1:numel(IDLabels)
    % Get the current matrix variable name
    current_var_name = IDLabels{matrixNumber};
    current_var_name_Time = IDLabelsTime{matrixNumber};

    %Going though each of the entires in the sample data  
    for index=1:1:size(data,1) 
        if strcmp(data.ID{index},  current_var_name )
                eval([current_var_name_Time ' = [' current_var_name_Time ', data.Time(index)];']);
                temp=str2double(data.Data(index));
                % str2double works, save the data 
            if isnan(temp) == 0 && isempty(temp) == 0
                eval([current_var_name ' = [' current_var_name ', temp];'])
                else 
                % Extract numeric values using regular expression
                numeric_values = regexp(data.Data(index), '\d+\.\d+', 'match');
                if isempty(numeric_values)==1 %If empty do it another way 
                    numeric_values = regexp(data.Data(index), '\d+\.\d?', 'match');
                end 
                %If none empty pick out the data
                if isempty(numeric_values) ==0 
                    for i = 1:numel(numeric_values)
                        temp(i,1) = str2double(numeric_values(1,i));
                    end
                    % Append to the end of the existing matrix
                    eval([current_var_name ' = [' current_var_name ', temp];']);
                else %Just add the data, noting do to it 
                   eval([current_var_name ' = [' current_var_name ', data.Data(index)];']);
                end 
            end   
        end
    end
end

%% Setting the start time to zero, by finding the minimum timestamp
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
    %Strubtacting the start time
    eval([current_matrix_name ' = [' current_matrix_name '-min_value];'])
end

%% Making struct to hold all the important data 

for matrixNumber = 1:numel(IDLabels)
    % Get the current matrix variable name
    current_var_name = IDLabels{matrixNumber};
    current_var_name_Time = IDLabelsTime{matrixNumber};
    log.(current_var_name)=eval(current_var_name); 
    log.(current_var_name_Time)=eval(current_var_name_Time); 
end 



end

