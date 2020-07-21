import pandas as pd
import gsw

DATES_COLUMNS = ['Date', 'Time']

class Data:
    def __init__(self, path):
        self._read(path)
        self._clean()

    def _read(self, path):
        self.data = pd.read_csv(path, sep='\s+', parse_dates=DATES_COLUMNS)
        for column in self.data.columns:
            if column not in DATES_COLUMNS:
                self.data[column].astype(float)

    def _clean(self):
        for_remove = []
        cur = 0

        for i in range(len(self.data)):
            if self.data.iloc[cur]['Pres'] > self.data.iloc[i]['Pres']:
                for_remove.append(self.data.index[i])
                continue
            else:
                removed = False

                for column in self.data.columns:
                    if column not in DATES_COLUMNS:
                        if self.data.iloc[i][column] < 1e-3:
                            for_remove.append(self.data.index[i])
                            removed = True
                            break

                if not removed:
                    cur = i

        self.data = self.data.drop(for_remove)

    def add_columns(self, columns):
        for column_name in columns:
            self.data[column_name] = columns[column_name]
            self.data[column_name].astype(float)


    def calc_teos10_columns(self, lat, lng):
        # Practical Salinity
        SP = gsw.SP_from_C(self.data['Cond'], self.data['Temp'], self.data['Pres'])
        # Absolute Salinity
        SA = gsw.SA_from_SP_Baltic(SP, lng, lat)
        # Conservative Temperature
        CT = gsw.CT_from_t(SA, self.data['Temp'], self.data['Pres'])
        # Sigma(density) with reference pressure of 0 dbar
        sigma = gsw.sigma0(SA, CT)
        # Depth 
        depth = list(map(abs, gsw.z_from_p(self.data['Pres'], lat)))

        return {'PracticalSalinity' : SP,
                'AbsoluteSalinity' : SA,
                'ConservativeTemperature' : CT,
                'Sigma(density)' : sigma,
                'Depth' : depth}

    def save_to_file(self, path):
        with open(path, 'w') as f:
            f.write(self._get_csv_string())

    def _get_csv_string(self):
        new_data = self.data.copy()
        new_data['Date'] = new_data['Date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        new_data['Time'] = new_data['Time'].apply(lambda x: x.strftime('%H:%M:%S.%f')[:11])
        return new_data.to_csv(sep=',', encoding='utf-8', index=False, float_format='%.3f')