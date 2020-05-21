using System.Collections.Generic;
using System.Data;
using System.Text;
using WatchmanWeb.Model;

namespace WatchmanWeb.Utility
{
    public static class TemplateGenerator
    {
        public static string GetHTMLString(List<Incident> incidents)
        {
            int lp = 1;
            DataTable dt = new DataTable();
            dt.Columns.AddRange(new DataColumn[4] {
                new DataColumn("Lp.",typeof(string)),
                new DataColumn("Data zdarzenia",typeof(string)),
                new DataColumn("Kategoria", typeof(string)),
                new DataColumn("Kamera",typeof(string))
             });

            incidents.ForEach(incident =>
            {
                dt.Rows.Add(
                    lp++,
                    incident.Timestamp,
                    incident.Flag,
                    incident.CameraInfo);
            });

            var sb = new StringBuilder();
            sb.AppendLine("<br/>");
            sb.AppendLine("<br/>");
            //Table wih datastart.
            sb.Append("<table cellpadding='5' cellspacing='0' style='border: 1px solid black;font-size: 30pt;font-family:Arial'>");

            //Adding HeaderRow.
            sb.Append("<tr>");
            foreach (DataColumn column in dt.Columns)
            {
                sb.Append("<th style='background-color: lightgrey;border: 1px solid black'>" + column.ColumnName + "</th>");
            }
            sb.Append("</tr>");


            //Adding DataRow.
            foreach (DataRow row in dt.Rows)
            {
                sb.Append("<tr>");
                foreach (DataColumn column in dt.Columns)
                {
                    sb.Append("<td style='width:100px;border: 1px solid #ccc'>" + row[column.ColumnName].ToString() + "</td>");
                }
                sb.Append("</tr>");
            }

            //Table end.
            sb.Append("</table>");
            return sb.ToString();
        }
    }
}
