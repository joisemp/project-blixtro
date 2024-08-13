import secrets
import string
from django.db.models import CharField

from apps.lab.models import Brand, Category, Item, Lab, System

def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


class LabElements:
  def __init__(self):
    lab_name = None
    room_no = None
    lab_incharge = None
    items = None
    systems = None
    categories = None
    brands = None
    dept = None
    
  def __str__(self):
    self.lab_name


def get_report_data(org):
  labs = Lab.objects.filter(org = org)
  context = {}
  labs_elements = []
  for lab in labs:
    ele = LabElements()
    ele.lab_name = lab.lab_name
    ele.room_no = lab.room_no
    ele.lab_incharge = lab.user.all()
    ele.dept = lab.dept.name
    ele.items = Item.objects.filter(lab=lab)
    ele.systems = System.objects.filter(lab=lab)
    ele.categories = Category.objects.filter(lab=lab)
    ele.brands = Brand.objects.filter(lab=lab)
    labs_elements.append(ele)

  return labs_elements

def get_lab_report_data(lab):
  ele = LabElements()
  ele.lab_name = lab.lab_name
  ele.room_no = lab.room_no
  ele.lab_incharge = lab.user.all()
  ele.dept = lab.dept.name
  ele.items = Item.objects.filter(lab=lab)
  ele.systems = System.objects.filter(lab=lab)
  ele.categories = Category.objects.filter(lab=lab)
  ele.brands = Brand.objects.filter(lab=lab)
  
  return ele



def get_lab_item_report_data(lab):
  ele = LabElements()
  ele.lab_name = lab.lab_name
  ele.room_no = lab.room_no
  ele.lab_incharge = lab.user.all()
  ele.dept = lab.dept.name
  ele.items = Item.objects.filter(lab=lab)
  
  return ele


def get_lab_system_report_data(lab):
  ele = LabElements()
  ele.lab_name = lab.lab_name
  ele.room_no = lab.room_no
  ele.lab_incharge = lab.user.all()
  ele.dept = lab.dept.name
  ele.systems = System.objects.filter(lab=lab)
  
  return ele

