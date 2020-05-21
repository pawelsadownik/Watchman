using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WatchmanWeb.Model
{
    public class Incident : Entity
    {
        public string Flag { get; set; }
        public DateTime Timestampt { get; set; }
        public string CameraInfo { get; set; }
    }
}
