# -*- coding: utf-8 -*-

from openerp import models, fields, api
import time
import datetime

# def utctolocal():
# from dateutil import tz
# from dateutil.tz import tzlocal
# from datetime import datetime
#     # get local time zone name
#     print datetime.now(tzlocal()).tzname()
#     # UTC Zone
#     from_zone = tz.gettz('UTC')
#     # China Zone
#     to_zone = tz.gettz('CST')
#     utc = datetime.utcnow()
#     print "utc:",utc
#     # Tell the datetime object that it's in UTC time zone
#     utc = utc.replace(tzinfo=from_zone)
#     # Convert time zone
#     local = utc.astimezone(to_zone)
#     print "local:",local

# utctolocal()

# def utc2local(utc_st):
#         #UTC时间转本地时间（+8:00）”“”
#         now_stamp = time.time()
#         local_time = datetime.datetime.fromtimestamp(now_stamp)
#         utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
#         print "local_time:",local_time
#         offset = local_time - utc_time
#         print "offset:",offset
#         local_st = utc_st + offset
#         print "local_st:",local_st
#         return local_st
#
# def local2utc(local_st):
#         #本地时间转UTC时间（-8:00）
#         time_struct = time.mktime(local_st.timetuple())
#         utc_st = datetime.datetime.utcfromtimestamp(time_struct)
#         return utc_st

class UfLogPrintReport(models.AbstractModel):
    _name = "report.ct_project_uf.uf_log_print_report"

    @api.multi
    def get_name(self):
        return [self.env['uf.log.print'].browse(self.ids)]

    @api.multi
    def get_alldata(self,docids):
        orderby = "id desc"
        # return self.env['uf.log.print'].search([], order=orderby)
        return self.env['uf.log.print'].search([('id','=',docids[0])], order=orderby)

    @api.multi
    def _formatDate(self, bdate, edate):
        # utctolocal()
        # datetime.strptime(lead.create_date, "%Y-%m-%d %H:%M:%S")
        if bdate and edate:
            # print "type(bdate):", type(bdate)
            # print "type(edate):", type(edate)
            # print "bdate:", bdate
            # print "edate:", edate
            # date to str
            # print time.strftime("%Y-%m-%d %X", time.localtime())
            # #str to date
            # t = time.strptime("2009 - 08 - 08", "%Y - %m - %d")
            # bdate = datetime.strptime(bdate, "%Y-%m-%d %H:%M:%S") 2016-12-22 01:00:58
            bdate = time.strptime(bdate, "%Y-%m-%d %H:%M:%S")
            edate = time.strptime(edate, "%Y-%m-%d %H:%M:%S")
            # print "type11111111111(bdate):", type(bdate)
            # print "bdate1111111111111:", bdate
            y, m, d, hour, min, sec = bdate[0:6]
            # print datetime.datetime(y,m,d,hour,min,sec)

            bdate = datetime.datetime(y, m, d, hour, min, sec) + datetime.timedelta(hours=8)
            y, m, d, hour, min, sec = edate[0:6]
            edate = datetime.datetime(y, m, d, hour, min, sec) + datetime.timedelta(hours=8)
            # print "bddddddddddddddddddddddddddddddddddate:", bdate
            # print "eddddddddddddddddddddddddddddddddddate:", edate
            # bstr = time.strftime("%Y-%m-%d %H:%M:%S",bdate)
            # estr = time.strftime("%Y-%m-%d %H:%M:%S",edate)
            # print "bstr:", bstr
            # print "estr:", estr
            return str(bdate)[11:16] + " - " + str(edate)[11:16]
        else:
            return ""

    @api.multi
    def _formatTime(self, bdate):
        if bdate:
            bdate = time.strptime(bdate, "%Y-%m-%d %H:%M:%S")
            y, m, d, hour, min, sec = bdate[0:6]
            bdate = datetime.datetime(y, m, d, hour, min, sec) + datetime.timedelta(hours=8)
            return str(bdate)[11:16]
        else:
            return ""

    @api.multi
    def update_impl(self,docids):
        print "self.ids:", self.ids
        #logprint = self.env['uf.log.print'].browse(self.ids)
        logprint = self.env['uf.log.print'].browse(docids[0])
        if not logprint:
            return

        logprint_id = logprint.id
        project_id = logprint.project_id.id
        sql = """update project_project set date_impl=
        (SELECT sum(impldate) from uf_log_print where project_id=%s)
        where id=%s""" % (project_id, project_id)
        print "sql:", sql
        self._cr.execute(sql)
        if not logprint.curdate or logprint.curdate == 0:
            cursql = """update uf_log_print set curdate=
                       (SELECT sum(impldate) from uf_log_print where project_id=%s)
                      where id=%s""" % (project_id, logprint_id)
            print "cursql:", cursql
            self._cr.execute(cursql)
            logprint.invalidate_cache()

    @api.multi
    def render_html(self,docids, data=None):
        self.update_impl(docids)
        print "docidsdocidsdocidsdocids:",docids
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ct_project_uf.uf_log_print_report')
        records =self.get_alldata(docids)
        #print "records:",records
        docargs = {
            "doc_ids": self.ids,
            "title":"日志预览",
            "doc_model": report.model,
            "docs": records,
            "format_date": self._formatDate,
            "format_time": self._formatTime,
        }
        return report_obj.render('ct_project_uf.uf_log_print_tpl', docargs)
