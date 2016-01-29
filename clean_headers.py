import os

data_dir = './sample_data/'

filenames = os.listdir(data_dir)

# do all the steps
def clean_headers(headers):
	unit_free = remove_units(header_list)
	qf_flag = rename_quality_flags(unit_free)
	return rename_date_time(qf_flag)


# who puts special characters in headers??
def rename_date_time(headers):
	clean_headers = []
	for item in headers:
		if item == 'mon/day/yr':
			clean_headers.append('Date')
		elif item == 'hh:mm':
			clean_headers.append('Time')
		else:
			clean_headers.append(item.strip())
	return clean_headers


# who puts special characters in headers??
def remove_units(headers):
	clean_headers = []
	for item in headers:
		if "[" in item:
			bracket_start = item.find('[')
			new_name = item[:bracket_start]
			clean_headers.append(new_name)
		else:
			clean_headers.append(item)

	return clean_headers


# QF fields renamed to contain the names of the fields they are a QF for
def rename_quality_flags(headers):
	clean_headers = []
	for idx, item in enumerate(headers):
		if item == 'QF':
			new_name = headers[idx-1] + ' QF'
			clean_headers.append(new_name)
		else:
			clean_headers.append(item)

	return clean_headers


cleaned_headers = 'clean_headers.csv'
with open(cleaned_headers, 'wb') as clean:
	for data_file in filenames:
		sample = data_dir + data_file 

		with open(sample, 'rb') as f:
			for line in f:
				if line[0] != '/':
					header = line.strip()  # remove carriage returns and newlines
					break 

		header_list = header.split("\t")  # fortunately the fields are tab-separated!
		final = clean_headers(header_list)

		# write the transormed headers to a file 
		numelem = len(final)
		for idx,item in enumerate(final):
			if idx == numelem - 1:
				clean.write("%s" % item)
			else:
				clean.write("%s," % item)

		clean.write('\n')