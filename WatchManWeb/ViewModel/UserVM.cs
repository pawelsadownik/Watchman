﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WatchmanWeb.ViewModel
{
    public class UserVM : EntityVM
    {
        public string UserName { get; set; }
        public string FirstName { get; set; }
        public string Password { get; set; }
        public string UserType { get; set; }
    }
}
