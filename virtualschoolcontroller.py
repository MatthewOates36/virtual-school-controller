import datetime
import json
import webbrowser

import rumps

weekDays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
schoolController = None
lastTime = None


class VirtualSchoolController(object):
    def __init__(self):
        self.config = {
            'app_name': 'Virtual School Controller',
            'join_class_title': 'Class Options'
        }
        self.app = rumps.App(self.config['app_name'], '📅')
        self.text = rumps.MenuItem(None)

        self.pauseButton = rumps.MenuItem(title='Pause', callback=self.pause)

        self.app.menu.add(self.text)

        self.app.menu.add(None)
        self.app.menu.add(rumps.MenuItem(title=self.config['join_class_title']))

        self.app.menu.add(None)
        self.app.menu.add(self.pauseButton)
        self.app.menu.add(rumps.MenuItem(title="Set config file path", callback=self.set_config_path))

        self.links = {}

        global weekDays
        global schoolController
        schoolController = self
        self.update()

    def run(self):
        self.app.run()

    @rumps.timer(15)
    def update(self):
        data = schoolController.read_json()

        today = datetime.datetime.now()

        next_event = None
        next_event_time = None
        next_event_time_data = None
        next_event_delta_time = 10000000000

        for key in schoolController.links.keys():
            schoolController.app.menu.pop(key)

        schoolController.links.clear()

        last_item = schoolController.config['join_class_title']
        for event in data:
            schoolController.links[event['name']] = event['link']
            schoolController.app.menu.insert_after(last_item,
                                                   rumps.MenuItem(title=event['name'],
                                                                  callback=schoolController.open_class_options))

            last_item = event['name']

            for time in event['times']:

                event_time = datetime.datetime.combine(
                    (today + datetime.timedelta((weekDays.index(str(time['dotw']).lower()) - today.weekday()) % 7)),
                    (datetime.datetime.strptime(time['time'], '%H:%M')).time())

                delta = (event_time - today).total_seconds()

                if 0 < delta < next_event_delta_time:
                    next_event = event
                    next_event_time = event_time
                    next_event_time_data = time
                    next_event_delta_time = delta

        if next_event is not None:

            time_information = ' at ' + next_event_time.strftime('%H:%M') + ' on ' + weekDays[
                next_event_time.weekday()].capitalize()

            if next_event_time.weekday() == today.weekday():
                timeuntil = int(next_event_delta_time / 60)
                if timeuntil < 2:
                    time_information = ' now'
                else:
                    hours = int(timeuntil / 60)
                    minutes = timeuntil % 60

                    hour_string = ''
                    minute_string = ''

                    if hours == 1:
                        hour_string = ' 1 hour'
                    elif hours > 1:
                        hour_string = ' ' + str(hours) + ' hours'

                    if minutes == 1:
                        minute_string = ' 1 minute'
                    elif minutes > 1:
                        minute_string = ' ' + str(minutes) + ' minutes'

                    if len(hour_string) > 0 and len(minute_string) > 0:
                        minute_string = ' and' + minute_string

                    time_information = ' at ' + next_event_time.strftime(
                        '%H:%M') + ' Today in' + hour_string + minute_string


            elif next_event_time.weekday() - today.weekday() == 1 or \
                    next_event_time.weekday() == 0 and today.weekday() == 6:
                time_information = ' at ' + next_event_time.strftime('%H:%M') + ' Tomorrow'

            schoolController.text.title = 'Your next class is ' + next_event['name'] + time_information
        else:
            schoolController.text.title = 'No classes found'

        current_time = today.strftime('%H:%M')

        global lastTime

        if current_time != lastTime and next_event is not None and schoolController.pauseButton.title.lower().startswith(
                'pause'):

            if 60 < next_event_time.timestamp() - today.timestamp() < 120:
                if next_event['link'] != '':
                    webbrowser.open(next_event['link'])

                if 'type' in next_event_time_data.keys() and next_event_time_data['type'] == 'temp':
                    next_event['times'].remove(next_event_time_data)
                    schoolController.write_json(data)

            elif 300 < next_event_time.timestamp() - today.timestamp() < 360:
                rumps.notification(schoolController.config['app_name'], None,
                                   "Get ready, you have " + next_event['name'] + " in 5 minutes", data=None,
                                   sound=True)

            elif 900 < next_event_time.timestamp() - today.timestamp() < 960:
                rumps.notification(schoolController.config['app_name'], None,
                                   "You have " + next_event['name'] + " in 15 minutes", data=None, sound=True)

            lastTime = current_time

    def read_json(self):
        file = None
        try:
            file = open(self.read_txt(), "r")
            data = json.loads(file.read())
        except Exception as e:
            return []
        finally:
            if file is not None:
                file.close()

        return data

    def write_json(self, data):
        try:
            file = open(self.read_txt(), "w")
            file.write(json.dumps(data, indent=2))
            file.close()
        except Exception as e:
            print(e)

    def read_txt(self):
        file = None
        try:
            file = open("config.txt", "r")

            data = file.read()
        except Exception as e:
            print(e)
            quit(-1)
        finally:
            if file is not None:
                file.close()

        return data

    def pause(self, sender):
        if sender.title.lower().startswith('pause'):
            self.pauseButton.title = 'Resume'
        else:
            self.pauseButton.title = 'Pause'

    def open_class_options(self, sender):
        window = rumps.Window(title=sender.title, ok='Cancel', dimensions=(0, 0))
        window.add_button('Add one time class')
        window.add_button('Join class now')

        response = window.run()

        if response.clicked == 2:
            self.add_one_time_event(sender)
        if response.clicked == 3:
            self.join_class(sender)

    def add_one_time_event(self, sender):
        window = rumps.Window(title=sender.title, message='Select Day/Time (HH:MM, 24 hour) for one time class',
                              ok='Cancel', dimensions=(200, 24))

        window.add_buttons('Sun', 'Sat', 'Fri', 'Thu', 'Wen', 'Tue', 'Mon')

        response = window.run()

        day = 8 - response.clicked

        if day < 7:
            try:
                datetime.datetime.strptime(response.text, '%H:%M').time()
            except Exception as e:
                rumps.Window(title='Error Parsing Date', message='Please try again', dimensions=(0, 0)).run()
                return

            data = self.read_json()

            for classData in data:
                if classData['name'] == sender.title:
                    classData['times'].append({'type': 'temp', 'dotw': weekDays[day], 'time': response.text})

            self.write_json(data)

    def join_class(self, sender):
        webbrowser.open(schoolController.links[sender.title])

    def set_config_path(self, sender):
        window = rumps.Window(title='Set config file path', message='Right click on the text box to paste',
                              default_text=self.read_txt(), cancel=True, dimensions=(400, 24))
        response = window.run()

        if response.clicked == 1:
            file = open("config.txt", "w")
            file.write(response.text)
            file.close()
            self.update()


if __name__ == '__main__':
    app = VirtualSchoolController()
    app.run()
