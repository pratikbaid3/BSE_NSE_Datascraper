import sqlite3

def latest_ca():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute('SELECT * FROM latest_nse_ca')
    ca_array=[]
    for data in c:
        corporate_action={
            'symbol':data[1],
            'company_name':data[2],
            'series':data[3],
            'face_value':data[4],
            'purpose':data[5],
            'ex_date':data[6],
            'record_date':data[7],
            'bc_start_date':data[8],
            'bc_end_date':data[9],
        }
        ca_array.append(corporate_action)

    conn.commit()
    conn.close()
    return ca_array
