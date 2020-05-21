using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WatchmanWeb.ViewModel
{
    public class IncidentVM : EntityVM
    {
        public string Flag { get; set; }
        public DateTime Timestamp { get; set; }
        public string CameraInfo { get; set; }
    }
}
