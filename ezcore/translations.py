from django.utils.translation import gettext_lazy as _

# Common translations for animal types
ANIMAL_TYPE_TRANSLATIONS = {
    'en': {
        'cow': 'Cow',
        'buffalo': 'Buffalo',
        'goat': 'Goat',
        'sheep': 'Sheep',
        'camel': 'Camel',
    },
    'ur': {
        'cow': 'گائے',
        'buffalo': 'بھینس',
        'goat': 'بکری',
        'sheep': 'بھیڑ',
        'camel': 'اونٹ',
    }
}

# Common translations for farming types
FARMING_TYPE_TRANSLATIONS = {
    'en': {
        'dairy': 'Dairy',
        'meat': 'Meat',
        'both': 'Both Dairy and Meat',
    },
    'ur': {
        'dairy': 'دودھ',
        'meat': 'گوشت',
        'both': 'دودھ اور گوشت دونوں',
    }
}

# Common translations for animal status
ANIMAL_STATUS_TRANSLATIONS = {
    'en': {
        'active': 'Active',
        'sold': 'Sold',
        'deceased': 'Deceased',
        'lactating': 'Lactating',
        'dry': 'Dry',
        'pregnant': 'Pregnant',
        'growing': 'Growing',
        'finishing': 'Finishing',
        'ready': 'Ready for slaughter',
    },
    'ur': {
        'active': 'فعال',
        'sold': 'فروخت شدہ',
        'deceased': 'فوت شدہ',
        'lactating': 'دودھ دینے والی',
        'dry': 'خشک',
        'pregnant': 'حاملہ',
        'growing': 'بڑھتی ہوئی',
        'finishing': 'تکمیل',
        'ready': 'ذبح کے لیے تیار',
    }
}

# Common translations for feed types
FEED_TYPE_TRANSLATIONS = {
    'en': {
        'forage': 'Forage',
        'concentrate': 'Concentrate',
        'supplement': 'Supplement',
        'mineral': 'Mineral',
    },
    'ur': {
        'forage': 'چارہ',
        'concentrate': 'کنسنٹریٹ',
        'supplement': 'اضافی خوراک',
        'mineral': 'معدنیات',
    }
}

# Common translations for health record types
HEALTH_RECORD_TRANSLATIONS = {
    'en': {
        'routine_check': 'Routine Check',
        'illness': 'Illness',
        'injury': 'Injury',
        'vaccination': 'Vaccination',
        'treatment': 'Treatment',
    },
    'ur': {
        'routine_check': 'معمول کا چیک اپ',
        'illness': 'بیماری',
        'injury': 'چوٹ',
        'vaccination': 'ویکسینیشن',
        'treatment': 'علاج',
    }
}

# Common translations for expense types
EXPENSE_TYPE_TRANSLATIONS = {
    'en': {
        'feed': 'Feed',
        'medicine': 'Medicine',
        'equipment': 'Equipment',
        'utilities': 'Utilities',
        'labor': 'Labor',
        'veterinary': 'Veterinary',
    },
    'ur': {
        'feed': 'خوراک',
        'medicine': 'دوا',
        'equipment': 'آلات',
        'utilities': 'یوٹیلیٹیز',
        'labor': 'مزدوری',
        'veterinary': 'ویٹرنری',
    }
}

# Common translations for UI elements
UI_TRANSLATIONS = {
    'en': {
        'dashboard': 'Dashboard',
        'animals': 'Animals',
        'dairy': 'Dairy',
        'meat': 'Meat',
        'health': 'Health',
        'feeding': 'Feeding',
        'inventory': 'Inventory',
        'sales': 'Sales',
        'expenses': 'Expenses',
        'reports': 'Reports',
        'settings': 'Settings',
        'logout': 'Logout',
        'profile': 'Profile',
        'add': 'Add',
        'edit': 'Edit',
        'delete': 'Delete',
        'save': 'Save',
        'cancel': 'Cancel',
        'search': 'Search',
        'filter': 'Filter',
        'export': 'Export',
        'import': 'Import',
    },
    'ur': {
        'dashboard': 'ڈیش بورڈ',
        'animals': 'جانور',
        'dairy': 'دودھ',
        'meat': 'گوشت',
        'health': 'صحت',
        'feeding': 'خوراک',
        'inventory': 'انوینٹری',
        'sales': 'فروخت',
        'expenses': 'اخراجات',
        'reports': 'رپورٹس',
        'settings': 'ترتیبات',
        'logout': 'لاگ آؤٹ',
        'profile': 'پروفائل',
        'add': 'شامل کریں',
        'edit': 'ترمیم کریں',
        'delete': 'حذف کریں',
        'save': 'محفوظ کریں',
        'cancel': 'منسوخ کریں',
        'search': 'تلاش کریں',
        'filter': 'فلٹر کریں',
        'export': 'برآمد کریں',
        'import': 'درآمد کریں',
    }
}
